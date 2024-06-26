import re
from typing import List, Dict, Any
import os
import sys

class SwiftStructClassParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.code = self._read_swift_file()
        self.lines = self.code.split('\n')
        self.type = self._determine_type()
        self.name = self._extract_name()
        self.attributes = self._extract_attributes()
        self.methods = self._extract_methods()
        self.parent_types = self._extract_parent_types()
        self.init_methods = self._extract_init_methods()

    def _read_swift_file(self) -> str:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def _determine_type(self) -> str:
        type_pattern = r'\b(class|struct)\b'
        for line in self.lines:
            match = re.search(type_pattern, line)
            if match:
                return match.group(1)
        raise ValueError("無法確定是 class 還是 struct")

    def _extract_name(self) -> str:
        name_pattern = rf'{self.type}\s+(\w+)'
        for line in self.lines:
            match = re.search(name_pattern, line)
            if match:
                return match.group(1)
        raise ValueError(f"無法找到 {self.type} 名稱")

    def _extract_attributes(self) -> List[str]:
        attributes = []
        var_pattern = r'\s*(var|let)\s+(\w+)(:.*)?'
        for line in self.lines:
            match = re.search(var_pattern, line)
            if match:
                attributes.append(line.strip())
        return attributes

    def _extract_methods(self) -> List[str]:
        methods = []
        func_pattern = r'\s*func\s+(\w+)\s*\((.*?)\)(\s*->\s*\S+)?'
        for line in self.lines:
            match = re.search(func_pattern, line)
            if match and not line.strip().startswith('init'):
                method_name = match.group(1)
                parameters = match.group(2)
                return_type = match.group(3) or ''
                method = f"func {method_name}({parameters}){return_type}"
                methods.append(method.strip())
        return methods

    def _extract_parent_types(self) -> List[str]:
        def_line = next(line for line in self.lines if self.type in line)
        parent_pattern = rf'{self.type}\s+\w+\s*:\s*(.*)'
        match = re.search(parent_pattern, def_line)
        if match:
            return [parent.strip() for parent in match.group(1).split(',')]
        return []

    def _extract_init_methods(self) -> List[str]:
        init_methods = []
        init_pattern = r'\s*init\s*\((.*?)\)'
        for line in self.lines:
            match = re.search(init_pattern, line)
            if match:
                parameters = match.group(1)
                init_method = f"init({parameters})"
                init_methods.append(init_method.strip())
        return init_methods

    def get_info(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'name': self.name,
            'attributes': self.attributes,
            'methods': self.methods,
            'parent_types': self.parent_types,
            'init_methods': self.init_methods
        }

def generate_html(info: Dict[str, Any]) -> str:
    html_template = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{type} {name} 3D 旋轉立方體圖表</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f0f8ff;
            perspective: 1000px;
        }}
        .scene {{
            width: 300px;
            height: 300px;
            perspective: 600px;
        }}
        .cube {{
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.5s;
        }}
        .cube__face {{
            position: absolute;
            width: 300px;
            height: 300px;
            border: 2px solid #333;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            padding: 10px;
            box-sizing: border-box;
            font-weight: bold;
            text-align: center;
            opacity: 0.8;
            overflow: auto;
        }}
        .cube__face--front  {{ background: #FF9AA2; transform: rotateY(  0deg) translateZ(150px); }}
        .cube__face--right  {{ background: #FFDAC1; transform: rotateY( 90deg) translateZ(150px); }}
        .cube__face--back   {{ background: #FFB7B2; transform: rotateY(180deg) translateZ(150px); }}
        .cube__face--left   {{ background: #E2F0CB; transform: rotateY(-90deg) translateZ(150px); }}
        .cube__face--top    {{ background: #B5EAD7; transform: rotateX( 90deg) translateZ(150px); }}
        .cube__face--bottom {{ background: #C7CEEA; transform: rotateX(-90deg) translateZ(150px); }}
        .type-name {{
            font-size: 24px;
            margin-bottom: 10px;
        }}
        .content {{
            font-size: 14px;
            text-align: left;
        }}
        .controls {{
            position: absolute;
            bottom: 20px;
            display: flex;
            gap: 10px;
        }}
        button {{
            padding: 10px 20px;
            background-color: #4682b4;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <div class="scene">
        <div class="cube">
            <div class="cube__face cube__face--front">
                <div class="type-name">{type} {name}</div>
                <div class="content">定義</div>
            </div>
            <div class="cube__face cube__face--back">
                <div class="type-name">方法</div>
                <div class="content">{methods}</div>
            </div>
            <div class="cube__face cube__face--right">
                <div class="type-name">屬性</div>
                <div class="content">{attributes}</div>
            </div>
            <div class="cube__face cube__face--left">
                <div class="type-name">初始化方法</div>
                <div class="content">{init_methods}</div>
            </div>
            <div class="cube__face cube__face--top">
                <div class="type-name">父類型</div>
                <div class="content">{parent_types}</div>
            </div>
            <div class="cube__face cube__face--bottom">
                <div class="type-name">子類型</div>
                <div class="content">無</div>
            </div>
        </div>
    </div>
    <div class="controls">
        <button id="rotateX">旋轉 X</button>
        <button id="rotateY">旋轉 Y</button>
        <button id="auto">自動旋轉</button>
    </div>

    <script>
        let cube = document.querySelector('.cube');
        let rotateX = 0, rotateY = 0;
        let autoRotate = false;

        function updateRotation() {{
            cube.style.transform = `rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg)`;
        }}

        document.getElementById('rotateX').addEventListener('click', () => {{
            rotateX += 90;
            updateRotation();
        }});

        document.getElementById('rotateY').addEventListener('click', () => {{
            rotateY += 90;
            updateRotation();
        }});

        document.getElementById('auto').addEventListener('click', () => {{
            autoRotate = !autoRotate;
            if (autoRotate) {{
                autoRotateAnimation();
            }}
        }});

        function autoRotateAnimation() {{
            if (autoRotate) {{
                rotateY += 1;
                updateRotation();
                requestAnimationFrame(autoRotateAnimation);
            }}
        }}

        // 滑鼠拖動旋轉
        let isDragging = false;
        let previousMousePosition = {{ x: 0, y: 0 }};

        document.addEventListener('mousedown', (e) => {{
            isDragging = true;
        }});

        document.addEventListener('mousemove', (e) => {{
            if (isDragging) {{
                let deltaMove = {{
                    x: e.clientX - previousMousePosition.x,
                    y: e.clientY - previousMousePosition.y
                }};
                rotateY += deltaMove.x * 0.5;
                rotateX -= deltaMove.y * 0.5;
                updateRotation();
            }}
            previousMousePosition = {{
                x: e.clientX,
                y: e.clientY
            }};
        }});

        document.addEventListener('mouseup', (e) => {{
            isDragging = false;
        }});
    </script>
</body>
</html>
    """
    return html_template.format(
        type=info['type'].capitalize(),
        name=info['name'],
        methods='<br>'.join(info['methods']),
        attributes='<br>'.join(info['attributes']),
        parent_types='<br>'.join(info['parent_types']) or '無',
        init_methods='<br>'.join(info['init_methods']) or '無'
    )

def swift_file_to_3d_cube(swift_file_path: str) -> None:
    try:
        parser = SwiftStructClassParser(swift_file_path)
        info = parser.get_info()
        html_content = generate_html(info)
        
        # 將生成的 HTML 保存到文件
        filename = f"{info['type']}_{info['name']}_3d_cube.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"3D 圖表已生成：{filename}")
    except Exception as e:
        print(f"生成 3D 圖表時發生錯誤：{str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法：python script_name.py <swift_file_name>")
        sys.exit(1)
    
    swift_file_name = sys.argv[1]
    if not swift_file_name.endswith('.swift'):
        swift_file_name += '.swift'
    
    if not os.path.exists(swift_file_name):
        print(f"錯誤：找不到文件 '{swift_file_name}'")
        sys.exit(1)
    
    swift_file_to_3d_cube(swift_file_name)
