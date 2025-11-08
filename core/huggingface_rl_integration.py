"""
HuggingFace Reinforcement Learning Integration
Integrates Stable-Baselines3 models for advanced game automation learning
"""

import logging
import numpy as np
from typing import Dict, Any, Optional, List
from pathlib import Path
import json

try:
    from stable_baselines3 import PPO, DQN, SAC, A2C
    from stable_baselines3.common.vec_env import DummyVecEnv
    from stable_baselines3.common.callbacks import BaseCallback
    STABLE_BASELINES_AVAILABLE = True
except ImportError:
    STABLE_BASELINES_AVAILABLE = False
    PPO = DQN = SAC = A2C = None

try:
    from huggingface_sb3 import load_from_hub, package_to_hub
    HUGGINGFACE_SB3_AVAILABLE = True
except ImportError:
    HUGGINGFACE_SB3_AVAILABLE = False

class LearningNotificationCallback(BaseCallback):
    """Callback for real-time learning notifications"""
    
    def __init__(self, notification_handler=None, verbose=0):
        super().__init__(verbose)
        self.notification_handler = notification_handler
        self.last_reward = 0
        self.episode_rewards = []
        
    def _on_step(self) -> bool:
        if self.notification_handler and len(self.episode_rewards) > 0:
            avg_reward = np.mean(self.episode_rewards[-10:])
            if avg_reward > self.last_reward + 0.1:
                self.notification_handler({
                    'type': 'improvement_detected',
                    'message': f'Performance improved! Avg reward: {avg_reward:.2f}',
                    'data': {'avg_reward': avg_reward, 'episode': self.num_timesteps}
                })
                self.last_reward = avg_reward
        return True
    
    def _on_rollout_end(self) -> None:
        if self.notification_handler:
            self.notification_handler({
                'type': 'training_progress',
                'message': f'Completed {self.num_timesteps} training steps',
                'data': {'timesteps': self.num_timesteps}
            })

class HuggingFaceRLIntegration:
    """Advanced RL integration using HuggingFace models"""
    
    def __init__(self, notification_handler=None):
        self.logger = logging.getLogger(__name__)
        self.notification_handler = notification_handler
        
        if not STABLE_BASELINES_AVAILABLE:
            self.logger.warning("Stable-Baselines3 not available. Install with: pip install stable-baselines3")
            self.enabled = False
            return
        
        self.enabled = True
        self.models = {}
        self.training_stats = {
            'total_timesteps': 0,
            'episodes_completed': 0,
            'best_reward': float('-inf'),
            'models_trained': 0,
            'improvements_detected': 0
        }
        
        self.models_dir = Path("data/rl_models")
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info("✓ HuggingFace RL Integration initialized with Stable-Baselines3")
    
    def load_pretrained_model(self, model_name: str, repo_id: str = None) -> Optional[Any]:
        """Load a pre-trained model from HuggingFace Hub"""
        if not self.enabled or not HUGGINGFACE_SB3_AVAILABLE:
            self.logger.warning("HuggingFace integration not available")
            return None
        
        try:
            checkpoint = load_from_hub(
                repo_id=repo_id or f"sb3/{model_name}",
                filename=f"{model_name}.zip"
            )
            
            if 'ppo' in model_name.lower():
                model = PPO.load(checkpoint)
            elif 'dqn' in model_name.lower():
                model = DQN.load(checkpoint)
            elif 'sac' in model_name.lower():
                model = SAC.load(checkpoint)
            elif 'a2c' in model_name.lower():
                model = A2C.load(checkpoint)
            else:
                model = PPO.load(checkpoint)
            
            self.models[model_name] = model
            
            if self.notification_handler:
                self.notification_handler({
                    'type': 'model_loaded',
                    'message': f'Loaded pre-trained model: {model_name}',
                    'data': {'model_name': model_name, 'source': 'HuggingFace Hub'}
                })
            
            self.logger.info(f"✓ Loaded pre-trained model: {model_name}")
            return model
            
        except Exception as e:
            self.logger.error(f"Failed to load pre-trained model {model_name}: {e}")
            return None
    
    def create_custom_model(self, model_type: str = 'PPO', policy: str = 'MlpPolicy',
                           learning_rate: float = 3e-4) -> Optional[Any]:
        """Create a new RL model for training"""
        if not self.enabled:
            return None
        
        try:
            model_classes = {
                'PPO': PPO,
                'DQN': DQN,
                'SAC': SAC,
                'A2C': A2C
            }
            
            if model_type not in model_classes:
                self.logger.error(f"Unknown model type: {model_type}")
                return None
            
            env = DummyVecEnv([lambda: GameAutomationEnv()])
            
            model = model_classes[model_type](
                policy,
                env,
                learning_rate=learning_rate,
                verbose=1
            )
            
            model_name = f"{model_type.lower()}_custom_{len(self.models)}"
            self.models[model_name] = model
            
            if self.notification_handler:
                self.notification_handler({
                    'type': 'model_created',
                    'message': f'Created new {model_type} model',
                    'data': {'model_type': model_type, 'learning_rate': learning_rate}
                })
            
            self.logger.info(f"✓ Created {model_type} model")
            return model
            
        except Exception as e:
            self.logger.error(f"Failed to create model: {e}")
            return None
    
    def train_model(self, model_name: str, total_timesteps: int = 10000):
        """Train a model with real-time notifications"""
        if not self.enabled or model_name not in self.models:
            return
        
        try:
            model = self.models[model_name]
            callback = LearningNotificationCallback(self.notification_handler)
            
            if self.notification_handler:
                self.notification_handler({
                    'type': 'training_started',
                    'message': f'Training {model_name} for {total_timesteps} steps',
                    'data': {'model_name': model_name, 'timesteps': total_timesteps}
                })
            
            model.learn(total_timesteps=total_timesteps, callback=callback)
            
            self.training_stats['total_timesteps'] += total_timesteps
            self.training_stats['models_trained'] += 1
            
            model_path = self.models_dir / f"{model_name}.zip"
            model.save(model_path)
            
            if self.notification_handler:
                self.notification_handler({
                    'type': 'training_completed',
                    'message': f'Training completed for {model_name}',
                    'data': {
                        'model_name': model_name,
                        'total_timesteps': total_timesteps,
                        'saved_path': str(model_path)
                    }
                })
            
            self.logger.info(f"✓ Training completed for {model_name}")
            
        except Exception as e:
            self.logger.error(f"Training error: {e}")
    
    def predict_action(self, model_name: str, observation) -> Optional[int]:
        """Get action prediction from model"""
        if not self.enabled or model_name not in self.models:
            return None
        
        try:
            model = self.models[model_name]
            action, _states = model.predict(observation, deterministic=True)
            return action
        except Exception as e:
            self.logger.error(f"Prediction error: {e}")
            return None
    
    def save_all_models(self):
        """Save all trained models"""
        for model_name, model in self.models.items():
            try:
                model_path = self.models_dir / f"{model_name}.zip"
                model.save(model_path)
                self.logger.info(f"Saved model: {model_name}")
            except Exception as e:
                self.logger.error(f"Failed to save {model_name}: {e}")
    
    def get_training_stats(self) -> Dict[str, Any]:
        """Get comprehensive training statistics"""
        return {
            **self.training_stats,
            'models_loaded': len(self.models),
            'enabled': self.enabled,
            'sb3_available': STABLE_BASELINES_AVAILABLE,
            'huggingface_available': HUGGINGFACE_SB3_AVAILABLE
        }


class GameAutomationEnv:
    """Minimal Gym-like environment for game automation"""
    
    def __init__(self):
        self.observation_space = None
        self.action_space = None
        self.current_state = None
    
    def reset(self):
        self.current_state = np.zeros(10)
        return self.current_state
    
    def step(self, action):
        reward = np.random.random()
        done = False
        info = {}
        self.current_state = np.random.random(10)
        return self.current_state, reward, done, info
    
    def render(self):
        pass
    
    def close(self):
        pass
