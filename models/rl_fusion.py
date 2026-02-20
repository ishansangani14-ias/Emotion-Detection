"""
Q-learning fusion agent for multimodal emotion detection
Learns which modality to trust based on confidence signals
"""
import os
import numpy as np
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import Config
from typing import Tuple


class RLFusionAgent:
    """Q-learning agent for modality fusion"""
    
    def __init__(self, config: Config):
        """
        Initialize Q-learning agent
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.q_table = np.zeros((config.NUM_STATES, config.NUM_ACTIONS))
        self.epsilon = config.Q_EPSILON
        self.episode_count = 0
    
    def determine_state(self, face_confidence: float, 
                       text_confidence: float) -> int:
        """
        Determine state based on confidence thresholds
        
        State 0: Both high (≥0.7)
        State 1: Face high (≥0.7), text low (<0.7)
        State 2: Face low (<0.7), text high (≥0.7)
        State 3: Both low (<0.7)
        
        Args:
            face_confidence: Face model confidence score
            text_confidence: Text model confidence score
        
        Returns:
            State index (0-3)
        """
        threshold = self.config.CONFIDENCE_THRESHOLD_HIGH
        
        face_high = face_confidence >= threshold
        text_high = text_confidence >= threshold
        
        if face_high and text_high:
            return 0
        elif face_high and not text_high:
            return 1
        elif not face_high and text_high:
            return 2
        else:
            return 3
    
    def select_action(self, state: int, epsilon: float = None) -> int:
        """
        Select action using epsilon-greedy policy
        
        Args:
            state: Current state index
            epsilon: Exploration rate (uses self.epsilon if None)
        
        Returns:
            Action index: 0 (FACE), 1 (TEXT), or 2 (AVERAGE)
        """
        if epsilon is None:
            epsilon = self.epsilon
        
        # Epsilon-greedy selection
        if np.random.random() < epsilon:
            # Explore: random action
            return np.random.randint(0, self.config.NUM_ACTIONS)
        else:
            # Exploit: best action
            return int(np.argmax(self.q_table[state]))
    
    def fuse_predictions(self, face_probs: np.ndarray, text_probs: np.ndarray,
                        action: int) -> Tuple[str, np.ndarray, str]:
        """
        Fuse predictions based on selected action
        
        Args:
            face_probs: Face model probability distribution
            text_probs: Text model probability distribution
            action: Selected action (0=FACE, 1=TEXT, 2=AVERAGE)
        
        Returns:
            Tuple of (final_emotion, final_probabilities, fusion_method)
        """
        action_names = ['FACE', 'TEXT', 'AVERAGE']
        fusion_method = action_names[action]
        
        if action == 0:  # FACE
            final_probs = face_probs
        elif action == 1:  # TEXT
            final_probs = text_probs
        else:  # AVERAGE
            final_probs = (face_probs + text_probs) / 2.0
        
        # Get final emotion
        emotion_idx = np.argmax(final_probs)
        final_emotion = self.config.EMOTIONS[emotion_idx]
        
        return final_emotion, final_probs, fusion_method
    
    def update_q_table(self, state: int, action: int, reward: float,
                      next_state: int):
        """
        Update Q-table using Q-learning algorithm
        
        Q(s,a) = Q(s,a) + α[r + γ*max(Q(s',a')) - Q(s,a)]
        
        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Next state
        """
        alpha = self.config.Q_LEARNING_RATE
        gamma = self.config.Q_DISCOUNT_FACTOR
        
        # Current Q-value
        old_q = self.q_table[state, action]
        
        # Best next Q-value
        max_next_q = np.max(self.q_table[next_state])
        
        # TD target
        td_target = reward + gamma * max_next_q
        
        # TD error
        td_error = td_target - old_q
        
        # Update Q-value
        new_q = old_q + alpha * td_error
        self.q_table[state, action] = new_q
        
        # Decay epsilon
        self.epsilon = max(
            self.config.Q_EPSILON_MIN,
            self.epsilon * self.config.Q_EPSILON_DECAY
        )
        
        self.episode_count += 1
        
        return old_q, new_q
    
    def compute_reward(self, predicted_emotion: str, 
                      true_emotion: str) -> float:
        """
        Compute reward based on prediction correctness
        
        Args:
            predicted_emotion: Predicted emotion label
            true_emotion: True emotion label
        
        Returns:
            Reward: 1.0 if correct, -1.0 if incorrect
        """
        return 1.0 if predicted_emotion == true_emotion else -1.0
    
    def get_q_table_display(self) -> str:
        """
        Return human-readable Q-table representation
        
        Returns:
            Formatted Q-table string
        """
        state_names = [
            "Both High (≥0.7)",
            "Face High, Text Low",
            "Face Low, Text High",
            "Both Low (<0.7)"
        ]
        action_names = ["FACE", "TEXT", "AVERAGE"]
        
        display = "\n" + "="*60 + "\n"
        display += "Q-TABLE (State-Action Values)\n"
        display += "="*60 + "\n\n"
        
        # Header
        display += f"{'State':<25} | "
        for action in action_names:
            display += f"{action:>10} | "
        display += f"{'Best Action':>12}\n"
        display += "-"*60 + "\n"
        
        # Rows
        for state_idx, state_name in enumerate(state_names):
            display += f"{state_name:<25} | "
            for action_idx in range(self.config.NUM_ACTIONS):
                q_val = self.q_table[state_idx, action_idx]
                display += f"{q_val:>10.4f} | "
            
            best_action = action_names[np.argmax(self.q_table[state_idx])]
            display += f"{best_action:>12}\n"
        
        display += "="*60 + "\n"
        display += f"Epsilon: {self.epsilon:.4f} | Episodes: {self.episode_count}\n"
        display += "="*60 + "\n"
        
        return display
    
    def save_q_table(self, path: str = None):
        """
        Save Q-table to disk
        
        Args:
            path: Path to save Q-table (defaults to config path)
        """
        if path is None:
            path = self.config.Q_TABLE_PATH
        
        # Create directory if needed
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Save Q-table and metadata
        data = {
            'q_table': self.q_table,
            'epsilon': self.epsilon,
            'episode_count': self.episode_count
        }
        np.save(path, data)
    
    def load_q_table(self, path: str = None):
        """
        Load Q-table from disk
        
        Args:
            path: Path to load Q-table from (defaults to config path)
        """
        if path is None:
            path = self.config.Q_TABLE_PATH
        
        if os.path.exists(path):
            data = np.load(path, allow_pickle=True).item()
            self.q_table = data['q_table']
            self.epsilon = data.get('epsilon', self.config.Q_EPSILON)
            self.episode_count = data.get('episode_count', 0)
        else:
            raise FileNotFoundError(f"Q-table file not found: {path}")
