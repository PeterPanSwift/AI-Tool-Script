import markdown
import re
from bs4 import BeautifulSoup
import argparse
import os

def markdown_to_disney_html(markdown_text, title):
    # Convert Markdown to HTML
    html = markdown.markdown(markdown_text, extensions=['tables'])
    
    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the table
    table = soup.find('table')
    
    if not table:
        return "No table found in the Markdown text."
    
    # Create the HTML structure
    html_structure = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap');

            body {{
                font-family: 'Nunito', sans-serif;
                background-color: #e6f3ff;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Cg fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.4'%3E%3Cpath opacity='.5' d='M96 95h4v1h-4v4h-1v-4h-9v4h-1v-4h-9v4h-1v-4h-9v4h-1v-4h-9v4h-1v-4h-9v4h-1v-4h-9v4h-1v-4h-9v4h-1v-4h-9v4h-1v-4H0v-1h15v-9H0v-1h15v-9H0v-1h15v-9H0v-1h15v-9H0v-1h15v-9H0v-1h15v-9H0v-1h15v-9H0v-1h15v-9H0v-1h15V0h1v15h9V0h1v15h9V0h1v15h9V0h1v15h9V0h1v15h9V0h1v15h9V0h1v15h9V0h1v15h9V0h1v15h4v1h-4v9h4v1h-4v9h4v1h-4v9h4v1h-4v9h4v1h-4v9h4v1h-4v9h4v1h-4v9h4v1h-4v9zm-1 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-9-10h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm9-10v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-9-10h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm9-10v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-9-10h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm9-10v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-9-10h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9z'/%3E%3Cpath d='M6 5V0H5v5H0v1h5v94h1V6h94V5H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
            }}
            .container {{
                background-color: #fff;
                border-radius: 30px;
                box-shadow: 0 0 30px rgba(0, 0, 0, 0.1);
                overflow: hidden;
                max-width: 800px;
                width: 95%;
                margin: 20px;
                position: relative;
            }}
            .container::before {{
                content: '';
                position: absolute;
                top: -20px;
                left: -20px;
                right: -20px;
                bottom: -20px;
                background: linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
                z-index: -1;
                border-radius: 40px;
                filter: blur(20px);
                opacity: 0.7;
            }}
            h1 {{
                text-align: center;
                color: #ff6b6b;
                margin: 30px 0;
                font-size: 32px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
            }}
            table {{
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                margin-bottom: 30px;
            }}
            th, td {{
                padding: 15px;
                text-align: left;
                border-bottom: 2px solid #e0e0e0;
                position: relative;
                overflow: hidden;
            }}
            th {{
                background-color: #feca57;
                color: white;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            tr:nth-child(even) {{
                background-color: #f0f8ff;
            }}
            tr:hover {{
                background-color: #e6f3ff;
                transform: scale(1.02);
                transition: all 0.3s ease;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            }}
            .swiftui {{
                color: #ff6b6b;
            }}
            .uikit {{
                color: #48dbfb;
            }}
            .mickey-ears::before,
            .mickey-ears::after {{
                content: '●';
                font-size: 20px;
                position: relative;
                top: -15px;
                margin: 0 10px;
            }}
            .sparkle {{
                position: absolute;
                background-color: white;
                width: 5px;
                height: 5px;
                border-radius: 50%;
                animation: twinkle 1.5s infinite;
            }}
            @keyframes twinkle {{
                0%, 100% {{ opacity: 0; transform: scale(0.5); }}
                50% {{ opacity: 1; transform: scale(1); }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="mickey-ears">{title}</h1>
            {table.prettify()}
        </div>
        <script>
            function createSparkle() {{
                const sparkle = document.createElement('div');
                sparkle.className = 'sparkle';
                sparkle.style.left = Math.random() * 100 + '%';
                sparkle.style.top = Math.random() * 100 + '%';
                sparkle.style.animationDelay = Math.random() * 2 + 's';
                document.querySelector('.container').appendChild(sparkle);
                setTimeout(() => sparkle.remove(), 1500);
            }}
            setInterval(createSparkle, 300);
        </script>
    </body>
    </html>
    """
    
    return html_structure

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown table to Disney-style HTML")
    parser.add_argument("input_file", help="Input Markdown file name")
    parser.add_argument("--title", default="Table", help="Title for the HTML page")
    args = parser.parse_args()

    # Read the Markdown file
    with open(args.input_file, 'r', encoding='utf-8') as f:
        markdown_text = f.read()

    # Convert Markdown to HTML
    html_output = markdown_to_disney_html(markdown_text, args.title)

    # Generate output file name
    base_name = os.path.splitext(args.input_file)[0]
    output_file = f"{base_name}_disney_style.html"

    # Save the HTML to a file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_output)

    print(f"HTML file has been generated: {output_file}")

if __name__ == "__main__":
    main()
