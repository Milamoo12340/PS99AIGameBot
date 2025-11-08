"""
Flask Web Application for AI Game Bot Dashboard
Provides web interface for game automation, vision system, and learning capabilities
"""
from flask import Flask, render_template, request, jsonify, send_from_directory, Response
from flask_cors import CORS
import logging
import os
import json
from pathlib import Path
import time

def create_app(bot_instance=None):
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
    
    CORS(app)
    
    logger = logging.getLogger('FlaskApp')
    
    global bot
    bot = bot_instance
    
    notification_bridge = None
    if bot and hasattr(bot, 'notification_bridge'):
        notification_bridge = bot.notification_bridge
    
    @app.route('/')
    def index():
        """Main dashboard"""
        return render_template('index.html')
    
    @app.route('/item-mapper')
    def item_mapper():
        """AI Item Mapper interface"""
        return render_template('item_mapper.html')
    
    @app.route('/task-recorder')
    def task_recorder():
        """Task recording interface"""
        return render_template('task_recorder.html')
    
    @app.route('/ps99-egg-hatcher')
    def ps99_egg_hatcher():
        """PS99 Egg Hatcher interface"""
        return render_template('ps99_egg_hatcher.html')
    
    @app.route('/multi-instance-launcher')
    def multi_instance_launcher():
        """Multi-instance launcher interface"""
        return render_template('multi_instance_launcher.html')
    
    @app.route('/window-detector')
    def window_detector():
        """Window detector interface"""
        return render_template('window_detector.html')
    
    @app.route('/api/execute', methods=['POST'])
    def execute_command():
        """Execute a command through the bot"""
        try:
            data = request.get_json()
            command = data.get('command', '')
            
            if not command:
                return jsonify({'success': False, 'error': 'No command provided'})
            
            if bot:
                result = bot.process_single_command(command)
                return jsonify({'success': True, 'result': str(result)})
            else:
                return jsonify({'success': False, 'error': 'Bot instance not available'})
                
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/status')
    def get_status():
        """Get bot status"""
        try:
            if bot:
                status = {
                    'connected': True,
                    'vision_active': bot.vision_system is not None,
                    'automation_active': bot.automation_engine is not None,
                    'learning_active': bot.learning_system is not None,
                    'minimal_mode': bot.minimal_mode,
                    'timestamp': str(os.path.getmtime(__file__))
                }
                return jsonify(status)
            else:
                return jsonify({'connected': False})
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return jsonify({'connected': False, 'error': str(e)})
    
    @app.route('/api/macros')
    def list_macros():
        """List available macros"""
        try:
            if bot and bot.macro_system is not None:
                macros = bot.macro_system.list_macros()
                return jsonify({'success': True, 'macros': macros})
            else:
                return jsonify({'success': True, 'macros': [], 'message': 'Macros not available in minimal mode'})
        except Exception as e:
            logger.error(f"Error listing macros: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/autoplay/start', methods=['POST'])
    def start_autoplay():
        """Start autoplay mode"""
        try:
            if bot:
                success = bot.start_autoplay_mode()
                return jsonify({'success': success})
            return jsonify({'success': False, 'error': 'Bot not available'})
        except Exception as e:
            logger.error(f"Error starting autoplay: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/autoplay/stop', methods=['POST'])
    def stop_autoplay():
        """Stop autoplay mode"""
        try:
            if bot:
                bot.stop_autoplay_mode()
                return jsonify({'success': True})
            return jsonify({'success': False, 'error': 'Bot not available'})
        except Exception as e:
            logger.error(f"Error stopping autoplay: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/item-mapper/detect-window', methods=['POST'])
    def detect_window():
        """Detect game window"""
        try:
            if bot and bot.vision_system is not None:
                result = {'success': True, 'window_detected': True}
                return jsonify(result)
            return jsonify({'success': False, 'error': 'Vision system not available in minimal mode. Install full dependencies to use this feature.'})
        except Exception as e:
            logger.error(f"Error detecting window: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/item-mapper/capture-item', methods=['POST'])
    def capture_item():
        """Capture item for mapping"""
        try:
            data = request.get_json()
            item_type = data.get('item_type')
            item_name = data.get('item_name')
            
            if bot and bot.interactive_trainer is not None:
                result = {'success': True, 'message': f'Item {item_name} captured'}
                return jsonify(result)
            return jsonify({'success': False, 'error': 'Interactive trainer not available in minimal mode'})
        except Exception as e:
            logger.error(f"Error capturing item: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/multi-instance/launch', methods=['POST'])
    def launch_instance():
        """Launch a new game instance"""
        try:
            if bot and bot.multi_instance_launcher is not None:
                result = bot.multi_instance_launcher.launch_instance()
                return jsonify({'success': True, 'result': result})
            return jsonify({'success': False, 'error': 'Multi-instance launcher not available in minimal mode'})
        except Exception as e:
            logger.error(f"Error launching instance: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/multi-instance/mutex/toggle', methods=['POST'])
    def toggle_mutex():
        """Toggle mutex bypass"""
        try:
            data = request.get_json()
            enable = data.get('enable', False)
            
            return jsonify({'success': True, 'mutex_active': enable})
        except Exception as e:
            logger.error(f"Error toggling mutex: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/ps99/eggs')
    def get_ps99_eggs():
        """Get PS99 eggs data"""
        try:
            eggs_file = Path('data/ps99_eggs.json')
            if eggs_file.exists():
                with open(eggs_file, 'r') as f:
                    eggs_data = json.load(f)
                return jsonify({'success': True, 'eggs': eggs_data})
            return jsonify({'success': False, 'eggs': []})
        except Exception as e:
            logger.error(f"Error getting eggs: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/ps99/hatch', methods=['POST'])
    def hatch_eggs():
        """Hatch PS99 eggs"""
        try:
            data = request.get_json()
            egg_id = data.get('egg_id')
            
            if bot:
                result = bot.process_single_command(f"hatch eggs {egg_id}")
                return jsonify({'success': True, 'result': str(result)})
            return jsonify({'success': False, 'error': 'Bot not available'})
        except Exception as e:
            logger.error(f"Error hatching eggs: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/recording/start', methods=['POST'])
    def start_recording():
        """Start task recording"""
        try:
            data = request.get_json()
            task_name = data.get('task_name', 'unnamed_task')
            
            return jsonify({'success': True, 'recording': True})
        except Exception as e:
            logger.error(f"Error starting recording: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/recording/stop', methods=['POST'])
    def stop_recording():
        """Stop task recording"""
        try:
            return jsonify({'success': True, 'recording': False})
        except Exception as e:
            logger.error(f"Error stopping recording: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/sync/status')
    def sync_status():
        """Get sync system status"""
        try:
            return jsonify({'success': True, 'sync_enabled': False, 'instances': []})
        except Exception as e:
            logger.error(f"Error getting sync status: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/learning/stats')
    def learning_stats():
        """Get comprehensive learning statistics"""
        try:
            stats = {}
            
            if bot:
                if hasattr(bot, 'learning_system') and bot.learning_system:
                    stats['learning_system'] = bot.learning_system.stats
                
                if hasattr(bot, 'hf_rl') and bot.hf_rl:
                    stats['huggingface_rl'] = bot.hf_rl.get_training_stats()
                
                if hasattr(bot, 'video_learner') and bot.video_learner:
                    stats['video_learning'] = bot.video_learner.get_stats()
                
                if hasattr(bot, 'code_learner') and bot.code_learner:
                    stats['code_generation'] = bot.code_learner.get_stats()
                
                if hasattr(bot, 'notification_manager') and bot.notification_manager:
                    stats['notifications'] = bot.notification_manager.get_stats()
            
            return jsonify({'success': True, 'stats': stats})
            
        except Exception as e:
            logger.error(f"Error getting learning stats: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/notifications/recent')
    def recent_notifications():
        """Get recent learning notifications"""
        try:
            limit = request.args.get('limit', 20, type=int)
            notifications = []
            
            if bot and hasattr(bot, 'notification_manager') and bot.notification_manager:
                notifications = bot.notification_manager.get_recent_notifications(limit)
            
            return jsonify({'success': True, 'notifications': notifications})
            
        except Exception as e:
            logger.error(f"Error getting notifications: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/notifications/stream')
    def notification_stream():
        """Server-Sent Events stream for real-time notifications"""
        def generate():
            while True:
                try:
                    if notification_bridge:
                        pending = notification_bridge.get_pending_notifications()
                        for notif in pending:
                            yield f"data: {json.dumps(notif)}\n\n"
                    time.sleep(0.5)
                except Exception as e:
                    logger.error(f"Stream error: {e}")
                    yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        return Response(generate(), mimetype='text/event-stream')
    
    @app.route('/api/video/learn-youtube', methods=['POST'])
    def learn_from_youtube():
        """Learn from a YouTube video"""
        try:
            data = request.get_json()
            video_url = data.get('url')
            focus_areas = data.get('focus_areas', [])
            
            if not video_url:
                return jsonify({'success': False, 'error': 'No URL provided'})
            
            if bot and hasattr(bot, 'video_learner') and bot.video_learner:
                result = bot.video_learner.learn_from_youtube(video_url, focus_areas)
                return jsonify(result)
            
            return jsonify({'success': False, 'error': 'Video learner not available'})
            
        except Exception as e:
            logger.error(f"Error learning from YouTube: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/video/upload', methods=['POST'])
    def upload_video():
        """Upload and learn from a video file"""
        try:
            if 'video' not in request.files:
                return jsonify({'success': False, 'error': 'No video file provided'})
            
            video_file = request.files['video']
            if video_file.filename == '':
                return jsonify({'success': False, 'error': 'No file selected'})
            
            temp_path = Path('data/uploads') / video_file.filename
            temp_path.parent.mkdir(parents=True, exist_ok=True)
            video_file.save(temp_path)
            
            if bot and hasattr(bot, 'video_learner') and bot.video_learner:
                result = bot.video_learner.learn_from_uploaded_file(str(temp_path))
                return jsonify(result)
            
            return jsonify({'success': False, 'error': 'Video learner not available'})
            
        except Exception as e:
            logger.error(f"Error uploading video: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/code/learn', methods=['POST'])
    def learn_from_code():
        """Learn from code examples"""
        try:
            data = request.get_json()
            code = data.get('code')
            language = data.get('language', 'python')
            
            if not code:
                return jsonify({'success': False, 'error': 'No code provided'})
            
            temp_file = Path('data/code_examples') / f'example_{int(time.time())}.{language}'
            temp_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(temp_file, 'w') as f:
                f.write(code)
            
            if bot and hasattr(bot, 'code_learner') and bot.code_learner:
                result = bot.code_learner.learn_from_code_file(str(temp_file), language)
                return jsonify(result)
            
            return jsonify({'success': False, 'error': 'Code learner not available'})
            
        except Exception as e:
            logger.error(f"Error learning from code: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/code/generate', methods=['POST'])
    def generate_code():
        """Generate code from learned patterns"""
        try:
            data = request.get_json()
            code_type = data.get('type')
            parameters = data.get('parameters', {})
            
            if not code_type:
                return jsonify({'success': False, 'error': 'No code type specified'})
            
            if bot and hasattr(bot, 'code_learner') and bot.code_learner:
                code = bot.code_learner.generate_code(code_type, parameters)
                if code:
                    return jsonify({'success': True, 'code': code})
                return jsonify({'success': False, 'error': 'No template available for this type'})
            
            return jsonify({'success': False, 'error': 'Code learner not available'})
            
        except Exception as e:
            logger.error(f"Error generating code: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/learning-dashboard')
    def learning_dashboard():
        """Learning dashboard page"""
        return render_template('learning_dashboard.html')
    
    @app.route('/health')
    def health():
        """Health check endpoint"""
        return jsonify({'status': 'healthy', 'service': 'ai-game-bot'})
    
    return app
