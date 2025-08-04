#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
마크다운 파일에서 단일 --- 라인을 제거하는 스크립트
"""

import os
import sys

def remove_single_dash_from_md_files(directory="."):
    """
    지정된 디렉토리의 모든 .md 파일에서 단일 --- 라인을 제거합니다.
    """
    md_files = []
    
    # .md 파일들을 찾습니다
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                # 비공개_로 시작하는 파일은 제외
                if file.startswith('비공개_'):
                    continue
                # .excalidraw.md 파일은 제외
                if file.endswith('.excalidraw.md'):
                    continue
                md_files.append(os.path.join(root, file))
    
    if not md_files:
        print("처리할 .md 파일을 찾을 수 없습니다.")
        return
    
    print(f"총 {len(md_files)}개의 .md 파일을 찾았습니다.")
    
    for file_path in md_files:
        process_md_file(file_path)

def process_md_file(file_path):
    """
    개별 .md 파일을 처리합니다.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 파일이 비어있는지 확인
        if not content.strip():
            print(f"✓ {file_path}: 빈 파일입니다.")
            return
        
        # 단일 --- 라인이 있는지 확인
        lines = content.split('\n')
        if len(lines) >= 1 and lines[0].strip() == '---':
            # 단일 --- 라인 제거
            new_content = remove_single_dash_from_content(content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✓ {file_path}: 단일 --- 라인을 제거했습니다.")
        else:
            print(f"✓ {file_path}: 단일 --- 라인이 없습니다.")
    
    except Exception as e:
        print(f"✗ {file_path}: 오류 발생 - {str(e)}")

def remove_single_dash_from_content(content):
    """
    내용에서 단일 --- 라인을 제거합니다.
    """
    lines = content.split('\n')
    
    # 첫 번째 라인이 ---인지 확인
    if len(lines) < 1 or lines[0].strip() != '---':
        return content
    
    # 첫 번째 --- 다음부터 시작
    result_lines = lines[1:]
    
    # 앞쪽 빈 줄 제거
    while result_lines and result_lines[0].strip() == '':
        result_lines = result_lines[1:]
    
    return '\n'.join(result_lines)

def main():
    """
    메인 함수
    """
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = "."
    
    if not os.path.exists(directory):
        print(f"오류: 디렉토리 '{directory}'가 존재하지 않습니다.")
        sys.exit(1)
    
    print(f"'{directory}' 디렉토리에서 .md 파일을 검색하고 단일 --- 라인을 제거합니다...")
    remove_single_dash_from_md_files(directory)
    print("완료되었습니다!")

if __name__ == "__main__":
    main() 