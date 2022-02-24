import pandas as pd
from tqdm import tqdm
import numpy as np

class Node(object):
    def __init__(self,key,left,right,height=0): # 기본 높이 0으로 설정
        self.key=key
        self.left=left
        self.right=right
        self.height=height

class Tree(object):
    def __init__(self):
        self.root = None 
    
    def node_height(self,node): # 노드의 높이 계산
        if node is None: # 비어있는 경우에 높이 -1로 계산 
            return -1
        else:
            return node.height
    
    def balance_factor(self,node): # balance factor 계산
        return self.node_height(node.left)-self.node_height(node.right)
    
    def insert(self,key):
        if self.root is None: # 루트 노드 없으면 만들기
            self.root = Node(key,None,None)
        else:
            self.root = self.insertion(key,self.root)
    
    def insertion(self, key, node):
        if node is None: # 내려가다가 그 자리에 비어있으면 삽입하기
            return Node(key,None,None)
        elif key[0] < node.key[0]: # 노드의 키보다 삽입하는 키가 작으면 왼쪽으로
            node.left = self.insertion(key,node.left)
        elif key[0] > node.key[0]: # 노드의 키보다 삽입하는 키가 크면 오른쪽으로
            node.right = self.insertion(key,node.right)
        
            
        node.height = max(self.node_height(node.left),self.node_height(node.right)) + 1 # 높이 업데이트
        bf = self.balance_factor(node) # balance factor 값 계산
        
        # -1 < bf < 1이 아니면 상황에 따라 회전
        
        if 1 < bf and key[0] < node.left.key[0]: # 왼쪽 자식, 왼쪽 서브트리에 추가
            node = self.r_rotation(node)
        elif -1 > bf and key[0] > node.right.key[0]: # 오른쪽 자식, 오른쪽 서브트리에 추가
            node = self.l_rotation(node)
        elif 1 < bf and key[0] > node.left.key[0]: # 왼쪽 자식, 오른쪽 서브트리에 추가
            node.left = self.l_rotation(node.left)
            node = self.r_rotation(node)
        elif -1 > bf and key[0] < node.right.key[0]: # 오른쪽 자식, 왼쪽 서브트리에 추가
            node.right = self.r_rotation(node.right)
            node = self.l_rotation(node)

        return node
    
    def l_rotation(self,node): # 왼쪽 회전
        alpha = node
        beta = node.right
        gamma = beta.left
        node = beta
        beta.left = alpha
        alpha.right = gamma
        
        alpha.height = max(self.node_height(alpha.left),self.node_height(alpha.right)) + 1 # 높이 업데이트
        beta.height = max(self.node_height(beta.left),self.node_height(beta.right)) + 1# 높이 업데이트
        # gamma는 높이 변화 없음
        return node
        
    def r_rotation(self,node): # 오른쪽 회전
        alpha = node
        beta = node.left
        gamma = beta.right
        node = beta
        beta.right = alpha
        alpha.left = gamma
        
        alpha.height = max(self.node_height(alpha.left),self.node_height(alpha.right)) + 1 # 높이 업데이트
        beta.height = max(self.node_height(beta.left),self.node_height(beta.right)) + 1# 높이 업데이트
        # gamma는 높이 변화 없음        
        return node
    
    def search_key(self,key,node):
        if key == node.key[0]: # 찾는 값이 일치하면
            key_find = node.key
            return key_find # (key, value) 쌍을 반환
        
        elif key < node.key[0]: # 노드의 키보다 검색하는 키가 작으면 왼쪽으로
            return self.search_key(key,node.left)
        
        elif key > node.key[0]: # 노드의 키보다 검색하는 키가 크면 오른쪽으로
            return self.search_key(key,node.right)
    

def main():
    tree=Tree()
    key_find = []
    value_find = []
    score = 0
    answer=int(input('원하는 입력을 입력하세요. : 1. insert 2. delete  3. quit\n'))
    
    while answer!=3:
        
        if answer == 1:
            file=input('파일 이름을 입력하세요. (확장자 명 포함)\t')
            data=pd.read_csv(file,header=None,sep='\t')
            input_key = data.iloc[:,0].values.tolist()
            input_value = data.iloc[:,1].values.tolist()
            print('삽입을 시작합니다.')

            for i in tqdm(range(data.shape[0])):
                tree.insert((input_key[i],input_value[i]))
            print('삽입이 완료되었습니다.')
            
            print('검색을 시작합니다.')
            for i in tqdm(range(data.shape[0])):   
                key = tree.search_key(input_key[i],tree.root)
                key_find.append(key[0])
                value_find.append(key[1])
                score += (key_find[i] == input_key[i]) & (value_find[i] == input_value[i])
            compare=pd.DataFrame([key_find,value_find]).T
            compare.to_csv('input_compare.csv',header=False,index=False,sep='\t')
            print('총 {0}개 중 {1}개를 맞췄습니다. 점수는 100점 중 {2}점 입니다.'.format(len(input_key),score,(score*100)/len(input_key)))
            answer=int(input('원하는 입력을 입력하세요. : 1. insert 2. search  3. quit\n'))

if __name__ == '__main__':
    main()      