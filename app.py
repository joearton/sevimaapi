"""
Flask Web Application untuk melihat response endpoint SEVIMA API
"""
import json
import os
import re
from flask import Flask, render_template, request, jsonify
from sevima_client import SEVIMAClient

app = Flask(__name__)

# Path untuk response.json
RESPONSE_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'response.json')

def extract_keys_only(data):
    """
    Extract hanya keys dari JSON response (structure only, no values)
    Recursively process dict, list, dan nested structures
    
    Contoh:
    Input: {"data": {"id": "123", "name": "John", "attrs": {"age": 30}}}
    Output: {"data": {"id": None, "name": None, "attrs": {"age": None}}}
    """
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if isinstance(value, dict):
                result[key] = extract_keys_only(value)
            elif isinstance(value, list):
                result[key] = extract_keys_only(value)
            else:
                # Primitive value (string, number, boolean, null)
                result[key] = None
        return result
    elif isinstance(data, list):
        if len(data) > 0:
            # Ambil struktur dari item pertama
            first_item = extract_keys_only(data[0])
            return [first_item] if first_item is not None else []
        else:
            # Empty list
            return []
    else:
        # Primitive value (string, number, boolean, null)
        return None

def save_response_structure(endpoint_path, response_data):
    """
    Simpan struktur response ke response.json
    Endpoint path sebagai key, struktur response sebagai value
    """
    # Load existing responses
    responses = {}
    if os.path.exists(RESPONSE_JSON_PATH):
        try:
            with open(RESPONSE_JSON_PATH, 'r', encoding='utf-8') as f:
                responses = json.load(f)
        except:
            responses = {}
    
    # Extract hanya keys dari response
    structure = extract_keys_only(response_data)
    
    # Simpan dengan endpoint path sebagai key
    responses[endpoint_path] = structure
    
    # Save ke file
    try:
        with open(RESPONSE_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(responses, f, indent=2, ensure_ascii=False)
        print(f"✅ Response structure saved for endpoint: {endpoint_path}")
    except Exception as e:
        print(f"❌ Error saving response structure: {e}")

# Load Postman collection
def load_endpoints():
    """Load dan parse endpoint dari Postman collection JSON"""
    endpoints = []
    
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, 'api_sevima_platform.json')
        
        with open(json_path, 'r', encoding='utf-8') as f:
            collection = json.load(f)
        
        def extract_endpoints(items, category="", subcategory=""):
            """Recursively extract endpoints from Postman collection"""
            for item in items:
                if 'item' in item:
                    # Ini adalah folder/kategori
                    name = item.get('name', '')
                    if category:
                        new_category = f"{category} > {name}"
                    else:
                        new_category = name
                    extract_endpoints(item['item'], new_category, subcategory)
                elif 'request' in item:
                    # Ini adalah endpoint
                    req = item.get('request', {})
                    method = req.get('method', 'GET')
                    url_obj = req.get('url', {})
                    
                    # Get path
                    if isinstance(url_obj.get('path'), list):
                        path = '/'.join(url_obj.get('path', []))
                    else:
                        path = url_obj.get('path', '')
                    
                    # Replace path variables (:id) dengan {id} untuk display
                    display_path = path.replace(':id', '{id}')
                    
                    # Get query parameters
                    query_params = []
                    if 'query' in url_obj and url_obj['query']:
                        for q in url_obj['query']:
                            if q.get('key'):
                                query_params.append(q.get('key'))
                    
                    # Get body untuk POST/PUT
                    body = None
                    if req.get('body'):
                        body_obj = req.get('body', {})
                        if body_obj.get('mode') == 'raw' and body_obj.get('raw'):
                            try:
                                body = json.loads(body_obj.get('raw', '{}'))
                            except:
                                body = body_obj.get('raw', '')
                    
                    # Get path variables
                    path_vars = []
                    if 'variable' in url_obj:
                        for var in url_obj['variable']:
                            if var.get('key'):
                                path_vars.append(var.get('key'))
                    
                    # Jika tidak ada di variable, extract dari path (untuk pattern :id, {id}, dll)
                    if not path_vars:
                        # Extract pattern :variable_name atau {variable_name}
                        pattern_matches = re.findall(r':(\w+)|{(\w+)}', path)
                        for match in pattern_matches:
                            var_name = match[0] if match[0] else match[1]
                            if var_name and var_name not in path_vars:
                                path_vars.append(var_name)
                    
                    # Pastikan path_vars selalu berupa list yang valid
                    if not isinstance(path_vars, list):
                        path_vars = []
                    
                    # Pastikan query_params selalu berupa list yang valid
                    if not isinstance(query_params, list):
                        query_params = []
                    
                    endpoints.append({
                        'name': item.get('name', ''),
                        'method': method,
                        'path': path,
                        'display_path': display_path,
                        'category': category,
                        'query_params': query_params,
                        'body': body,
                        'path_vars': path_vars if path_vars else [],  # Pastikan selalu list, bukan None
                        'description': item.get('description', '')
                    })
        
        if 'item' in collection:
            extract_endpoints(collection['item'])
        
        # Sort endpoints by category and method
        endpoints.sort(key=lambda x: (x['category'], x['method'], x['path']))
        
    except Exception as e:
        print(f"Error loading endpoints: {e}")
    
    return endpoints

# Cache endpoints
ENDPOINTS = load_endpoints()

def get_client():
    """Get SEVIMA client instance"""
    try:
        return SEVIMAClient()
    except ValueError as e:
        return None

@app.route('/')
def index():
    """Home page - tampilkan daftar semua endpoint"""
    # Group endpoints by category
    categories = {}
    for endpoint in ENDPOINTS:
        cat = endpoint['category'] or 'Lainnya'
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(endpoint)
    
    return render_template('index.html', categories=categories, total=len(ENDPOINTS))

@app.route('/api/endpoints')
def api_endpoints():
    """API endpoint untuk mendapatkan list endpoint"""
    return jsonify(ENDPOINTS)

@app.route('/api/documentation')
def api_documentation():
    """API endpoint untuk mendapatkan dokumentasi response"""
    try:
        if os.path.exists(RESPONSE_JSON_PATH):
            with open(RESPONSE_JSON_PATH, 'r', encoding='utf-8') as f:
                documentation = json.load(f)
            return jsonify({
                'success': True,
                'documentation': documentation
            })
        else:
            return jsonify({
                'success': True,
                'documentation': {},
                'message': 'Belum ada dokumentasi. Test beberapa endpoint terlebih dahulu.'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/documentation')
def documentation_page():
    """Halaman dokumentasi response"""
    return render_template('documentation.html')

@app.route('/api/test', methods=['POST'])
def test_endpoint():
    """Test endpoint dan return response"""
    try:
        data = request.get_json()
        endpoint_path = data.get('path', '')
        method = data.get('method', 'GET').upper()
        path_params = data.get('path_params', {})
        query_params = data.get('query_params', {})
        body_data = data.get('body', {})
        
        # Replace path variables
        actual_path = endpoint_path
        for key, value in path_params.items():
            actual_path = actual_path.replace(f':{key}', value)
            actual_path = actual_path.replace(f'{{{key}}}', value)
        
        # Initialize client
        client = get_client()
        if not client:
            return jsonify({
                'success': False,
                'error': 'Client tidak dapat diinisialisasi. Pastikan SEVIMA_API_KEY dan SEVIMA_SECRET_KEY sudah di-set di file .env'
            }), 400
        
        # Execute request based on method
        try:
            if method == 'GET':
                response = client.get(actual_path, params=query_params if query_params else None)
            elif method == 'POST':
                response = client.post(actual_path, json=body_data if body_data else None)
            elif method == 'PUT':
                response = client.put(actual_path, json=body_data if body_data else None)
            elif method == 'DELETE':
                response = client.delete(actual_path)
            else:
                return jsonify({
                    'success': False,
                    'error': f'Method {method} tidak didukung'
                }), 400
            
            # Simpan struktur response ke response.json
            # Gunakan actual_path sebagai key (endpoint path)
            if response:
                save_response_structure(actual_path, response)
            
            return jsonify({
                'success': True,
                'response': response,
                'endpoint': actual_path,
                'method': method
            })
        
        except Exception as e:
            import traceback
            error_detail = str(e)
            try:
                # Try to get response body if it's an HTTP error
                if hasattr(e, 'response') and e.response:
                    error_detail = e.response.text
            except:
                pass
            
            return jsonify({
                'success': False,
                'error': error_detail,
                'traceback': traceback.format_exc()
            }), 400
            
    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

if __name__ == '__main__':
    print(f"Total endpoints loaded: {len(ENDPOINTS)}")
    print("Starting Flask server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
