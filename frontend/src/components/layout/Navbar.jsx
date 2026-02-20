import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
  const location = useLocation();
  
  const navItems = [
    { path: '/', label: '📊 Dashboard', icon: '📊' },
    { path: '/realtime', label: '📷 Real-Time', icon: '📷' },
    { path: '/upload', label: '📤 Upload', icon: '📤' },
    { path: '/text', label: '💬 Text', icon: '💬' },
    { path: '/history', label: '📜 History', icon: '📜' },
    { path: '/analytics', label: '📈 Analytics', icon: '📈' },
    { path: '/rl-viz', label: '🧠 RL Viz', icon: '🧠' },
    { path: '/insights', label: '🔍 Insights', icon: '🔍' },
    { path: '/theory', label: '📚 Theory', icon: '📚' },
    { path: '/settings', label: '⚙️ Settings', icon: '⚙️' },
  ];
  
  return (
    <nav className="bg-bg-secondary border-b border-border-primary">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-2">
            <span className="text-3xl">🎭</span>
            <h1 className="text-xl font-bold text-primary">
              Emotion Intelligence Platform
            </h1>
          </div>
          
          <div className="flex space-x-1">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  location.pathname === item.path
                    ? 'bg-primary text-white'
                    : 'text-text-secondary hover:bg-bg-tertiary hover:text-text-primary'
                }`}
              >
                <span className="mr-1">{item.icon}</span>
                {item.label.split(' ')[1]}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
