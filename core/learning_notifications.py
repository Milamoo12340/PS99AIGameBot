"""
Real-time Learning Notification System
Provides visual feedback for AI learning events
"""

import logging
import time
import json
from typing import Dict, Any, List, Callable
from collections import deque
from pathlib import Path
import threading

class LearningNotificationManager:
    """Manages real-time notifications for learning events"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.notifications = deque(maxlen=100)
        self.listeners = []
        self.stats = {
            'total_notifications': 0,
            'by_type': {},
            'recent_events': []
        }
        
        self.notification_lock = threading.Lock()
        self.logger.info("✓ Learning Notification Manager initialized")
    
    def notify(self, notification: Dict[str, Any]):
        """Send a learning notification"""
        with self.notification_lock:
            timestamp = time.time()
            notification['timestamp'] = timestamp
            notification['id'] = f"notif_{int(timestamp * 1000)}"
            
            self.notifications.append(notification)
            self.stats['total_notifications'] += 1
            
            notif_type = notification.get('type', 'unknown')
            self.stats['by_type'][notif_type] = self.stats['by_type'].get(notif_type, 0) + 1
            
            self.stats['recent_events'].append({
                'type': notif_type,
                'message': notification.get('message', ''),
                'timestamp': timestamp
            })
            
            if len(self.stats['recent_events']) > 20:
                self.stats['recent_events'] = self.stats['recent_events'][-20:]
            
            for listener in self.listeners:
                try:
                    listener(notification)
                except Exception as e:
                    self.logger.error(f"Listener error: {e}")
            
            self.logger.info(f"📢 {notif_type}: {notification.get('message', '')}")
    
    def add_listener(self, callback: Callable):
        """Add a notification listener"""
        self.listeners.append(callback)
    
    def remove_listener(self, callback: Callable):
        """Remove a notification listener"""
        if callback in self.listeners:
            self.listeners.remove(callback)
    
    def get_recent_notifications(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent notifications"""
        with self.notification_lock:
            return list(self.notifications)[-limit:]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get notification statistics"""
        return {
            **self.stats,
            'active_listeners': len(self.listeners),
            'notifications_in_memory': len(self.notifications)
        }
    
    def notify_item_learned(self, item_name: str, item_type: str, confidence: float = 0.0):
        """Notify when AI learns a new item"""
        self.notify({
            'type': 'item_learned',
            'category': 'learning',
            'message': f'🎯 Learned new {item_type}: {item_name}',
            'data': {
                'item_name': item_name,
                'item_type': item_type,
                'confidence': confidence
            },
            'priority': 'high'
        })
    
    def notify_pattern_discovered(self, pattern_name: str, occurrences: int):
        """Notify when AI discovers a pattern"""
        self.notify({
            'type': 'pattern_discovered',
            'category': 'learning',
            'message': f'🔍 Discovered pattern: {pattern_name} ({occurrences} occurrences)',
            'data': {
                'pattern_name': pattern_name,
                'occurrences': occurrences
            },
            'priority': 'medium'
        })
    
    def notify_performance_improvement(self, task: str, old_score: float, new_score: float):
        """Notify when performance improves"""
        improvement = ((new_score - old_score) / old_score * 100) if old_score > 0 else 0
        self.notify({
            'type': 'performance_improvement',
            'category': 'progress',
            'message': f'📈 {task} improved by {improvement:.1f}%',
            'data': {
                'task': task,
                'old_score': old_score,
                'new_score': new_score,
                'improvement_percent': improvement
            },
            'priority': 'high'
        })
    
    def notify_watching(self, activity: str):
        """Notify that AI is actively watching"""
        self.notify({
            'type': 'watching',
            'category': 'status',
            'message': f'👁️ Watching: {activity}',
            'data': {'activity': activity},
            'priority': 'low'
        })
    
    def notify_memory_saved(self, memory_type: str, count: int):
        """Notify when memories are saved"""
        self.notify({
            'type': 'memory_saved',
            'category': 'storage',
            'message': f'💾 Saved {count} {memory_type} memories',
            'data': {
                'memory_type': memory_type,
                'count': count
            },
            'priority': 'low'
        })
    
    def notify_strategy_adapted(self, strategy_name: str, reason: str):
        """Notify when AI adapts a strategy"""
        self.notify({
            'type': 'strategy_adapted',
            'category': 'learning',
            'message': f'🎮 Adapted strategy: {strategy_name}',
            'data': {
                'strategy_name': strategy_name,
                'reason': reason
            },
            'priority': 'medium'
        })
    
    def notify_object_detected(self, object_type: str, location: Dict[str, int], confidence: float):
        """Notify when object is detected"""
        self.notify({
            'type': 'object_detected',
            'category': 'vision',
            'message': f'🎯 Detected {object_type} (confidence: {confidence:.2f})',
            'data': {
                'object_type': object_type,
                'location': location,
                'confidence': confidence
            },
            'priority': 'low'
        })
    
    def notify_learning_from_video(self, source: str, frames_analyzed: int):
        """Notify when learning from video"""
        self.notify({
            'type': 'video_learning',
            'category': 'learning',
            'message': f'🎥 Learning from video: {source} ({frames_analyzed} frames)',
            'data': {
                'source': source,
                'frames_analyzed': frames_analyzed
            },
            'priority': 'medium'
        })
    
    def notify_code_generated(self, code_type: str, lines: int):
        """Notify when code is generated"""
        self.notify({
            'type': 'code_generated',
            'category': 'generation',
            'message': f'💻 Generated {code_type} code ({lines} lines)',
            'data': {
                'code_type': code_type,
                'lines': lines
            },
            'priority': 'medium'
        })


class BrowserNotificationBridge:
    """Bridges learning notifications to browser via WebSocket/SSE"""
    
    def __init__(self, notification_manager: LearningNotificationManager):
        self.notification_manager = notification_manager
        self.logger = logging.getLogger(__name__)
        self.notification_queue = deque(maxlen=50)
        
        notification_manager.add_listener(self._handle_notification)
        self.logger.info("✓ Browser notification bridge initialized")
    
    def _handle_notification(self, notification: Dict[str, Any]):
        """Handle incoming notification and prepare for browser"""
        browser_notification = {
            'id': notification.get('id'),
            'type': notification.get('type'),
            'category': notification.get('category', 'info'),
            'title': self._get_notification_title(notification),
            'message': notification.get('message', ''),
            'timestamp': notification.get('timestamp'),
            'priority': notification.get('priority', 'medium'),
            'data': notification.get('data', {})
        }
        
        self.notification_queue.append(browser_notification)
    
    def _get_notification_title(self, notification: Dict[str, Any]) -> str:
        """Get user-friendly notification title"""
        titles = {
            'item_learned': '🎯 New Item Learned',
            'pattern_discovered': '🔍 Pattern Discovered',
            'performance_improvement': '📈 Performance Improved',
            'watching': '👁️ AI Watching',
            'memory_saved': '💾 Memory Saved',
            'strategy_adapted': '🎮 Strategy Adapted',
            'object_detected': '🎯 Object Detected',
            'video_learning': '🎥 Learning from Video',
            'code_generated': '💻 Code Generated',
            'training_started': '🚀 Training Started',
            'training_completed': '✅ Training Complete',
            'model_loaded': '📦 Model Loaded',
            'improvement_detected': '⚡ Improvement Detected'
        }
        return titles.get(notification.get('type'), '📢 AI Update')
    
    def get_pending_notifications(self) -> List[Dict[str, Any]]:
        """Get all pending browser notifications"""
        notifications = list(self.notification_queue)
        self.notification_queue.clear()
        return notifications
