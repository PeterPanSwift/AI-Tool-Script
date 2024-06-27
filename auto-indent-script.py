import sys

def auto_indent(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        indent_level = 0
        for line in infile:
            stripped_line = line.strip()
            
            # 減少縮排的情況
            if stripped_line.startswith('}') or stripped_line.startswith(']') or stripped_line.startswith(')'):
                indent_level = max(0, indent_level - 1)
            
            # 寫入縮排後的行
            outfile.write('    ' * indent_level + stripped_line + '\n')
            
            # 增加縮排的情況
            if stripped_line.endswith('{') or stripped_line.endswith('[') or stripped_line.endswith('('):
                indent_level += 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法: python auto_indent.py <輸入文件> <輸出文件>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    auto_indent(input_file, output_file)
    print(f"縮排完成。結果已保存到 {output_file}")
