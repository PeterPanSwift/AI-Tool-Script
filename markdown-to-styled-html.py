import markdown
import sys
import re

def markdown_table_to_html(markdown_text):
    # 將 Markdown 轉換為 HTML
    html = markdown.markdown(markdown_text, extensions=['tables'])
    
    # 提取表格內容
    table_pattern = r'<table>(.*?)</table>'
    table_match = re.search(table_pattern, html, re.DOTALL)
    
    if not table_match:
        return "No table found in the Markdown text."
    
    table_content = table_match.group(1)
    
    # 創建完整的 HTML 頁面
    styled_html = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>酷炫現代風格的表格</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

            body {{
                font-family: 'Roboto', sans-serif;
                line-height: 1.6;
                color: #e0e0e0;
                max-width: 1000px;
                margin: 0 auto;
                padding: 40px 20px;
                background-color: #121212;
                background-image: 
                    linear-gradient(45deg, #1a1a1a 25%, transparent 25%),
                    linear-gradient(-45deg, #1a1a1a 25%, transparent 25%),
                    linear-gradient(45deg, transparent 75%, #1a1a1a 75%),
                    linear-gradient(-45deg, transparent 75%, #1a1a1a 75%);
                background-size: 20px 20px;
            }}
            h1 {{
                color: #bb86fc;
                text-align: center;
                margin-bottom: 40px;
                font-weight: 700;
                letter-spacing: 2px;
                text-transform: uppercase;
                text-shadow: 0 0 10px rgba(187, 134, 252, 0.7);
            }}
            table {{
                width: 100%;
                border-collapse: separate;
                border-spacing: 0 15px;
                background-color: transparent;
            }}
            th, td {{
                padding: 20px;
                text-align: left;
                background-color: #1e1e1e;
                transition: all 0.3s ease;
            }}
            th {{
                background-color: #03dac6;
                color: #000000;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-size: 16px;
                clip-path: polygon(5% 0%, 100% 0%, 95% 100%, 0% 100%);
            }}
            tr {{
                transform: perspective(1000px) rotateX(0deg);
                transition: transform 0.3s ease;
            }}
            tr:hover {{
                transform: perspective(1000px) rotateX(5deg);
                z-index: 10;
            }}
            td {{
                position: relative;
                overflow: hidden;
            }}
            td::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
                transform: translateX(-100%);
                transition: 0.5s;
            }}
            tr:hover td::before {{
                transform: translateX(100%);
            }}
            @media screen and (max-width: 768px) {{
                table {{
                    font-size: 14px;
                }}
                th, td {{
                    padding: 15px;
                }}
            }}
        </style>
    </head>
    <body>
        <h1>酷炫現代風格的表格</h1>
        <table>
            {table_content}
        </table>
    </body>
    </html>
    """
    
    return styled_html

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <markdown_file>")
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    
    try:
        with open(markdown_file, 'r', encoding='utf-8') as file:
            markdown_text = file.read()
        
        html_output = markdown_table_to_html(markdown_text)
        
        output_file = markdown_file.rsplit('.', 1)[0] + '_styled.html'
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(html_output)
        
        print(f"Styled HTML has been saved to {output_file}")
    
    except FileNotFoundError:
        print(f"Error: File '{markdown_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
