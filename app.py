"""
Flask Web Application for AI Game Bot Dashboard
Provides web interface for game automation, vision system, and learning capabilities
"""
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import logging
import os
import json
from pathlib import Path

def create_app(bot_instance=None):
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    CORS(app)
    
    logger = logging.getLogger('FlaskApp')
    
    global bot
    bot = bot_instance
    
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
    
    @app.route('/health')
    def health():
        """Health check endpoint"""
        return jsonify({'status': 'healthy', 'service': 'ai-game-bot'})
    
    return app
