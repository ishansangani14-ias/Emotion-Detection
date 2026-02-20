"""
Reinforcement Learning API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List

from backend.database import get_db, Detection, RLTraining
from backend.schemas import FeedbackRequest, FeedbackResponse
from backend.services import detection_service
from backend.config import settings

router = APIRouter()


@router.get("/rl/qtable")
async def get_qtable():
    """
    Get current Q-table state
    
    - Returns Q-table values, states, actions, epsilon, and episodes
    """
    rl_agent = detection_service.rl_agent
    
    state_names = [
        "Both High (≥0.7)",
        "Face High, Text Low",
        "Face Low, Text High",
        "Both Low (<0.7)"
    ]
    action_names = ["Trust Face", "Trust Text", "Average Both"]
    
    # Convert Q-table to list of lists
    qtable_list = rl_agent.q_table.tolist()
    
    # Find best action for each state
    best_actions = []
    for state_idx in range(len(state_names)):
        best_action_idx = int(rl_agent.q_table[state_idx].argmax())
        best_actions.append(action_names[best_action_idx])
    
    return {
        "qtable": qtable_list,
        "states": state_names,
        "actions": action_names,
        "best_actions": best_actions,
        "epsilon": float(rl_agent.epsilon),
        "episodes": int(rl_agent.episode_count)
    }


@router.post("/rl/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    request: FeedbackRequest,
    db: Session = Depends(get_db)
):
    """
    Submit feedback for Q-learning update
    
    - **detection_id**: ID of the detection
    - **correct_emotion**: The correct emotion label
    - **predicted_emotion**: The predicted emotion label
    - **state**: RL state (optional)
    - **action**: RL action (optional)
    - Returns feedback confirmation and Q-table update status
    """
    # Get detection from database
    detection = db.query(Detection).filter(Detection.id == request.detection_id).first()
    
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    
    # Compute reward
    is_correct = request.correct_emotion == request.predicted_emotion
    reward = 1.0 if is_correct else -1.0
    
    # Update detection record
    detection.is_correct = is_correct
    detection.correct_emotion = request.correct_emotion
    
    # Update Q-table if multimodal
    q_table_updated = False
    if detection.mode == "multimodal" and detection.rl_state is not None:
        rl_agent = detection_service.rl_agent
        
        state = detection.rl_state
        action = detection.rl_action
        
        # Determine next state (same as current for terminal state)
        next_state = state
        
        # Update Q-table
        old_q, new_q = rl_agent.update_q_table(state, action, reward, next_state)
        
        # Save Q-table
        rl_agent.save_q_table()
        
        # Log training episode
        training_log = RLTraining(
            episode=rl_agent.episode_count,
            state=state,
            action=action,
            reward=reward,
            q_value_before=old_q,
            q_value_after=new_q,
            epsilon=rl_agent.epsilon
        )
        db.add(training_log)
        
        q_table_updated = True
    
    db.commit()
    
    return FeedbackResponse(
        message="Feedback received successfully",
        q_table_updated=q_table_updated,
        reward=reward
    )


@router.get("/rl/training-history")
async def get_training_history(
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get RL training history
    
    - **limit**: Maximum number of records to return
    - Returns list of training episodes with rewards and Q-values
    """
    history = db.query(RLTraining).order_by(
        RLTraining.timestamp.desc()
    ).limit(limit).all()
    
    return [
        {
            "episode": h.episode,
            "state": h.state,
            "action": h.action,
            "reward": h.reward,
            "q_value_before": h.q_value_before,
            "q_value_after": h.q_value_after,
            "epsilon": h.epsilon,
            "timestamp": h.timestamp
        }
        for h in history
    ]


@router.get("/rl/reward-trend")
async def get_reward_trend(
    episodes: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get reward trend over last N episodes
    
    - **episodes**: Number of episodes to analyze
    - Returns list of rewards over time
    """
    history = db.query(RLTraining).order_by(
        RLTraining.episode.desc()
    ).limit(episodes).all()
    
    # Reverse to get chronological order
    history = list(reversed(history))
    
    return [
        {
            "episode": h.episode,
            "reward": h.reward,
            "epsilon": h.epsilon
        }
        for h in history
    ]
