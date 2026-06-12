#!/usr/bin/env python3
"""web占卜 · Flask 主程序"""
import sys, os
from flask import Flask, render_template, request, jsonify

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from xiaoliuren import compute as xiaoliuren_compute
from meihua import compute as meihua_compute
from liuyao import compute as liuyao_compute
from qimen import compute as qimen_compute
from liuren import compute as liuren_compute

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/xiaoliuren', methods=['POST'])
def api_xiaoliuren():
    try:
        data = request.get_json()
        result = xiaoliuren_compute(
            int(data.get('month', 1)),
            int(data.get('day', 1)),
            data.get('hour_name', '子')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/meihua', methods=['POST'])
def api_meihua():
    try:
        data = request.get_json()
        result = meihua_compute(
            data.get('method', 'number'),
            data.get('values', {})
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/liuyao', methods=['POST'])
def api_liuyao():
    try:
        data = request.get_json()
        result = liuyao_compute(
            data.get('lines', []),
            data.get('question_type', '其他'),
            data.get('sex', '男')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route('/api/qimen', methods=['POST'])
def api_qimen():
    try:
        data = request.get_json()
        result = qimen_compute(
            int(data.get('year', 2026)), int(data.get('month', 6)),
            int(data.get('day', 13)), int(data.get('hour', 12)),
            data.get('q_type', '考试')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/liuren', methods=['POST'])
def api_liuren():
    try:
        data = request.get_json()
        result = liuren_compute(
            int(data.get('year', 2026)), int(data.get('month', 6)),
            int(data.get('day', 13)), int(data.get('hour', 12)),
            data.get('q_type', '其他')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
