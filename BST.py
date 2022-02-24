import pandas as pd
import sys
from tqdm import tqdm
sys.setrecursionlimit(10**6)

class Node(object):
    def __init__(self,key,left,right):
        self.key=key
        self.left=left
        self.right=right

class Tree(object):
    def __init__(self):
        self.root=None
    
    def insertion(self,key,node):
        self.now = self.root # 현재 노드를 루트노드로 설정
        while True:
            if key[0] < self.now.key[0]: # 노드의 키보다 삽입하는 키가 작으면 왼쪽으로 내려가기
                if self.now.left is None :
                    self.now.left = Node(key,None,None)
                    break
                else:
                    self.now=self.now.left # 현재 노드를 왼쪽 자식 노드로 변경
                
            elif key[0] > self.now.key[0] : # 노드의 키보다 삽입하는 키가 크면 오른쪽으로 내려가기
                if self.now.right is None:
                    self.now.right = Node(key,None,None)
                    break
                else:
                    self.now=self.now.right # 현재 노드를 오른쪽 자식 노드로 변경
        
    def insert(self,key):
        if self.root is None: # 루트노드 없으면 만들기
            self.root = Node(key,None,None)
        else:
            return self.insertion(key,self.root)
        
    def search_key(self,key,node):
        self.now = self.root
        while True:
            if key == self.now.key[0]: # 찾는 값이 일치하면
                key_find=self.now.key
                return key_find  # (key, value) 쌍을 반환
            
            elif key < self.now.key[0] : # 노드의 키보다 검색하는 키가 작으면
                self.now = self.now.left
            
            elif key > self.now.key[0]: # 노드의 키보다 검색하는 키가 크면
                self.now = self.now.right
            
    
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