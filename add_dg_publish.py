#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
마크다운 파일에 dg-publish: true 추가하는 간단한 스크립트
frontmatter가 없을 때만 추가합니다.
"""

import os
import sys

def add_dg_publish_to_md_files(directory="."):
    """
    지정된 디렉토리의 모든 .md 파일에 dg-publish: true를 추가합니다.
    frontmatter가 없을 때만 추가합니다.
    """
    md_files = []
    
    # .md 파일들을 찾습니다
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                # 비공개_로 시작하는 파일은 제외
                if file.startswith('비공개_'):
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
        
        # frontmatter가 있는지 확인 (---로 시작하는지)
        lines = content.split('\n')
        if lines and lines[0].strip() == '---':
            print(f"✓ {file_path}: frontmatter가 이미 있습니다.")
            return
        
        # frontmatter가 없으면 dg-publish 추가
        new_content = f"---\ndg-publish: true\n---\n\n{content}"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ {file_path}: dg-publish: true를 추가했습니다.")
    
    except Exception as e:
        print(f"✗ {file_path}: 오류 발생 - {str(e)}")

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
    
    print(f"'{directory}' 디렉토리에서 .md 파일을 검색하고 dg-publish를 추가합니다...")
    add_dg_publish_to_md_files(directory)
    print("완료되었습니다!")

if __name__ == "__main__":
    main() 