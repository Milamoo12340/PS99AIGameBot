"""
Video Learning System
Learn from YouTube videos and uploaded video files
"""

import logging
import cv2
import numpy as np
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
import tempfile
import subprocess

try:
    from pytube import YouTube
    PYTUBE_AVAILABLE = True
except ImportError:
    PYTUBE_AVAILABLE = False

class VideoLearningSystem:
    """System for learning from video content"""
    
    def __init__(self, notification_manager=None):
        self.logger = logging.getLogger(__name__)
        self.notification_manager = notification_manager
        
        self.learned_patterns = []
        self.video_cache = Path("data/video_cache")
        self.video_cache.mkdir(parents=True, exist_ok=True)
        
        self.frame_skip = 5
        self.max_frames_per_video = 1000
        
        self.stats = {
            'videos_processed': 0,
            'frames_analyzed': 0,
            'patterns_learned': 0,
            'actions_identified': 0
        }
        
        self.logger.info("✓ Video Learning System initialized")
    
    def learn_from_youtube(self, video_url: str, focus_areas: List[str] = None) -> Dict[str, Any]:
        """Learn from a YouTube video"""
        if not PYTUBE_AVAILABLE:
            self.logger.error("pytube not available. Install with: pip install pytube")
            return {'success': False, 'error': 'pytube not installed'}
        
        try:
            if self.notification_manager:
                self.notification_manager.notify_watching(f"YouTube video: {video_url}")
            
            yt = YouTube(video_url)
            
            video_stream = yt.streams.filter(file_extension='mp4', res="360p").first()
            if not video_stream:
                video_stream = yt.streams.filter(file_extension='mp4').first()
            
            if not video_stream:
                return {'success': False, 'error': 'No suitable video stream found'}
            
            video_path = video_stream.download(output_path=str(self.video_cache))
            
            result = self._analyze_video_file(video_path, focus_areas)
            
            self.stats['videos_processed'] += 1
            
            if self.notification_manager:
                self.notification_manager.notify_learning_from_video(
                    source=yt.title,
                    frames_analyzed=result.get('frames_analyzed', 0)
                )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error learning from YouTube: {e}")
            return {'success': False, 'error': str(e)}
    
    def learn_from_uploaded_file(self, file_path: str, focus_areas: List[str] = None) -> Dict[str, Any]:
        """Learn from an uploaded video file"""
        try:
            if not Path(file_path).exists():
                return {'success': False, 'error': 'File not found'}
            
            if self.notification_manager:
                self.notification_manager.notify_watching(f"Uploaded video: {Path(file_path).name}")
            
            result = self._analyze_video_file(file_path, focus_areas)
            
            self.stats['videos_processed'] += 1
            
            if self.notification_manager:
                self.notification_manager.notify_learning_from_video(
                    source=Path(file_path).name,
                    frames_analyzed=result.get('frames_analyzed', 0)
                )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error learning from file: {e}")
            return {'success': False, 'error': str(e)}
    
    def _analyze_video_file(self, video_path: str, focus_areas: List[str] = None) -> Dict[str, Any]:
        """Analyze video file frame by frame"""
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                return {'success': False, 'error': 'Could not open video file'}
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps if fps > 0 else 0
            
            frames_analyzed = 0
            patterns_found = []
            actions_detected = []
            
            frame_count = 0
            while cap.isOpened() and frames_analyzed < self.max_frames_per_video:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % self.frame_skip == 0:
                    analysis = self._analyze_frame(frame, focus_areas)
                    
                    if analysis.get('patterns'):
                        patterns_found.extend(analysis['patterns'])
                    
                    if analysis.get('actions'):
                        actions_detected.extend(analysis['actions'])
                    
                    frames_analyzed += 1
                
                frame_count += 1
            
            cap.release()
            
            self.stats['frames_analyzed'] += frames_analyzed
            self.stats['patterns_learned'] += len(set(patterns_found))
            self.stats['actions_identified'] += len(set(actions_detected))
            
            unique_patterns = list(set(patterns_found))
            for pattern in unique_patterns[:5]:
                if self.notification_manager:
                    self.notification_manager.notify_pattern_discovered(
                        pattern_name=pattern,
                        occurrences=patterns_found.count(pattern)
                    )
            
            return {
                'success': True,
                'frames_analyzed': frames_analyzed,
                'total_frames': total_frames,
                'duration': duration,
                'fps': fps,
                'patterns_found': unique_patterns,
                'actions_detected': list(set(actions_detected)),
                'learning_summary': self._generate_learning_summary(unique_patterns, actions_detected)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing video: {e}")
            return {'success': False, 'error': str(e)}
    
    def _analyze_frame(self, frame: np.ndarray, focus_areas: List[str] = None) -> Dict[str, Any]:
        """Analyze a single video frame"""
        patterns = []
        actions = []
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        if edge_density > 0.1:
            patterns.append('high_activity')
        
        brightness = np.mean(gray)
        if brightness > 200:
            patterns.append('bright_ui')
        elif brightness < 50:
            patterns.append('dark_scene')
        
        if focus_areas:
            for area in focus_areas:
                if area.lower() in ['chest', 'egg', 'button']:
                    patterns.append(f'{area}_detection_attempt')
        
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 10:
            actions.append('interaction_likely')
        
        return {
            'patterns': patterns,
            'actions': actions,
            'metadata': {
                'brightness': float(brightness),
                'edge_density': float(edge_density),
                'contours': len(contours)
            }
        }
    
    def _generate_learning_summary(self, patterns: List[str], actions: List[str]) -> str:
        """Generate a human-readable learning summary"""
        summary_parts = []
        
        if patterns:
            summary_parts.append(f"Identified {len(patterns)} unique visual patterns")
        
        if actions:
            summary_parts.append(f"Detected {len(actions)} action types")
        
        if 'chest' in ' '.join(patterns).lower():
            summary_parts.append("Learned chest opening behaviors")
        
        if 'egg' in ' '.join(patterns).lower():
            summary_parts.append("Learned egg hatching sequences")
        
        return ". ".join(summary_parts) if summary_parts else "Basic visual patterns learned"
    
    def get_stats(self) -> Dict[str, Any]:
        """Get video learning statistics"""
        return {
            **self.stats,
            'patterns_in_library': len(self.learned_patterns),
            'pytube_available': PYTUBE_AVAILABLE
        }
    
    def save_learned_patterns(self):
        """Save learned patterns to disk"""
        try:
            patterns_file = Path("data/video_learned_patterns.json")
            with open(patterns_file, 'w') as f:
                json.dump({
                    'patterns': self.learned_patterns,
                    'stats': self.stats
                }, f, indent=2)
            
            if self.notification_manager:
                self.notification_manager.notify_memory_saved(
                    memory_type='video_patterns',
                    count=len(self.learned_patterns)
                )
            
        except Exception as e:
            self.logger.error(f"Failed to save patterns: {e}")


class CodeGenerationLearner:
    """Learn to generate code from examples"""
    
    def __init__(self, notification_manager=None):
        self.logger = logging.getLogger(__name__)
        self.notification_manager = notification_manager
        
        self.code_templates = {}
        self.learned_patterns = {}
        
        self.stats = {
            'code_examples_analyzed': 0,
            'templates_created': 0,
            'code_generated': 0
        }
        
        self.logger.info("✓ Code Generation Learner initialized")
    
    def learn_from_code_file(self, file_path: str, language: str = 'python') -> Dict[str, Any]:
        """Learn from a code file"""
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            
            patterns = self._extract_code_patterns(code, language)
            
            for pattern_type, pattern_code in patterns.items():
                if pattern_type not in self.code_templates:
                    self.code_templates[pattern_type] = []
                self.code_templates[pattern_type].append(pattern_code)
            
            self.stats['code_examples_analyzed'] += 1
            self.stats['templates_created'] += len(patterns)
            
            return {
                'success': True,
                'patterns_found': len(patterns),
                'pattern_types': list(patterns.keys())
            }
            
        except Exception as e:
            self.logger.error(f"Error learning from code: {e}")
            return {'success': False, 'error': str(e)}
    
    def _extract_code_patterns(self, code: str, language: str) -> Dict[str, str]:
        """Extract reusable patterns from code"""
        patterns = {}
        
        if language == 'python':
            if 'def ' in code:
                patterns['function_definition'] = "def function_name():\n    pass"
            if 'class ' in code:
                patterns['class_definition'] = "class ClassName:\n    pass"
            if 'for ' in code:
                patterns['for_loop'] = "for item in items:\n    pass"
            if 'if ' in code:
                patterns['conditional'] = "if condition:\n    pass"
        
        return patterns
    
    def generate_code(self, code_type: str, parameters: Dict[str, Any] = None) -> Optional[str]:
        """Generate code based on learned patterns"""
        if code_type not in self.code_templates:
            return None
        
        template = self.code_templates[code_type][0] if self.code_templates[code_type] else None
        
        if template and parameters:
            for key, value in parameters.items():
                template = template.replace(f'{{{key}}}', str(value))
        
        self.stats['code_generated'] += 1
        
        if self.notification_manager and template:
            lines = template.count('\n') + 1
            self.notification_manager.notify_code_generated(
                code_type=code_type,
                lines=lines
            )
        
        return template
    
    def get_stats(self) -> Dict[str, Any]:
        """Get code generation statistics"""
        return {
            **self.stats,
            'template_types': len(self.code_templates)
        }
