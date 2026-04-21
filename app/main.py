from flask import Blueprint, jsonify, request
from app.database import db
from app.models import Item

api_bp = Blueprint('api', __name__, url_prefix='/api')


# ── Health Check ──────────────────────────────────────
@api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    try:
        # Query database to verify connection
        Item.query.first()
        return jsonify({'status': 'ok', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ── Items Endpoints ──────────────────────────────────────
@api_bp.route('/items', methods=['GET'])
def get_all_items():
    """Retrieve all items from database."""
    try:
        items = Item.query.all()
        return jsonify([item.to_dict() for item in items]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Retrieve a specific item by ID."""
    try:
        item = Item.query.get_or_404(item_id)
        return jsonify(item.to_dict()), 200
    except Exception as e:
        return jsonify({'error': 'Item not found'}), 404


@api_bp.route('/items', methods=['POST'])
def create_item():
    """Create a new item in the database."""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({'error': 'Name field is required'}), 400
        
        new_item = Item(
            name=data['name'],
            description=data.get('description', None)
        )
        
        db.session.add(new_item)
        db.session.commit()
        
        return jsonify({
            'message': 'Item created successfully',
            'item': new_item.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update an existing item."""
    try:
        item = Item.query.get_or_404(item_id)
        data = request.get_json()
        
        if 'name' in data:
            item.name = data['name']
        if 'description' in data:
            item.description = data['description']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Item updated ver successfully',
            'item': item.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item from the database."""
    try:
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({'message': 'Item deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ── Root Endpoint ──────────────────────────────────────
@api_bp.route('/', methods=['GET'])
def root():
    """Root API endpoint."""
    return jsonify({
        'name': 'Flask MySQL API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'items': '/api/items',
            'item_detail': '/api/items/<id>',
            'docs': '/docs'
        }
    }), 200


# ── Root with app context ──────────────────────────────────────
if __name__ == '__main__':
    from app import create_app
    app = create_app()
    app.run(host='0.0.0.0', port=80, debug=False)  # nosec B104
