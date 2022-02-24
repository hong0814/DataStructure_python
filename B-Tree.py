import pandas as pd
from tqdm import tqdm
import sys
import numpy as np
sys.setrecursionlimit(10**4)
class Node(object):
    def __init__(self,keys, childs, leaf=False):
        self.keys=keys
        self.childs=childs
        self.leaf=leaf
    # 대소 비교 용
    def __lt__(self, other):
        return (self.keys < other.keys)

    def __gt__(self, other):
        return (self.keys > other.keys) 
    
class Tree(object):
    def __init__(self,M):
        self.M=M         # M차 B_Tree
        self.root = Node([],[],True) # 리프인 노드
        self.min_key = round(M/2)-1  # 최소 키 개수
        self.max_key = M-1           # 최대 키 개수
        
    def insert(self,key):
        root=self.root
        self.insertion(key,root)
        if len(root.keys) > self.max_key: # 최대 키 개수 넘어가면
            new_root = Node([],[],leaf=False)
            self.root=new_root # 새로운 노드를 루트노드로 선언
            new_root.childs.append(root)
            self.split_node(new_root,0)

    def insertion(self,key,node): 
        i=0
        if node.leaf:   # 노드가 리프노드일 때 
            if node.keys != []:    
                while key[0] > node.keys[i][0]:
                    i=i+1
                    if i+1 > len(node.keys):
                        break
            node.keys.append(key)
            node.keys.sort()

        
        else:         # 노드가 리프노드가 아닐 때    
            if node.keys != []:           
                while key[0] > node.keys[i][0]:
                    i=i+1
                    if i+1 > len(node.keys):
                        break
            self.insertion(key,node.childs[i])
            
            if len(node.childs[i].keys) > self.max_key: # 삽입하고 나서 자식노드가 최대 키 개수 넘어가면
                self.split_node(node,i)      # 자식노드 분할 시행    
   

    def split_node(self,node,index):     # 자식노드 분할
        children = node.childs[index]
        median = len(children.keys)//2  # 자식노드의 중앙값 index
        medoid = children.keys[median] # 중앙값 key, value 쌍
        
        if children.leaf: # 자식노드가 리프노드이면
            new=Node([],[],leaf=True)            
            node.childs.insert(index+1,new)
            node.keys.append(medoid)
            node.keys.sort()
            new.keys.extend(children.keys[median+1:])
            children.keys = children.keys[:median]
            
        
        else: # 자식노드가 리프노드 아니면
            new=Node([],[],leaf=False)            
            node.childs.insert(index+1,new)
            node.keys.append(medoid)
            node.keys.sort()
            new.keys.extend(children.keys[median+1:])
            children.keys = children.keys[:median] 
            
            new.childs.extend(children.childs[median+1:])
            children.childs = children.childs[:median+1]           

    def search_key(self,key,node): # key를 검색해서, key-value 쌍 가져오기
        i=0
        while key > node.keys[i][0]:
            i=i+1
            if i > len(node.keys)-1:
                break
        
        node_keys= [j[0] for j in node.keys] # 노드의 키들만 담은 리스트

        if key in node_keys:
            idx=node_keys.index(key)
            key_find, value_find = node.keys[idx][0], node.keys[idx][1]
            return key_find, value_find
       
        else:
            try:
                return self.search_key(key,node.childs[i])    
            except:
                key_find, value_find = key, np.nan
                return key_find, value_find
                  
    def location(self, node, key): # 원래가 i이면 key는 i-1, childs는 i
        a=0
        b=len(node.childs)-1
        while a<b:
            k = (a+b+1)//2
            if node.keys[k-1] <= key: 
                a=k
            else:
                b = k-1
        return a           

    def delete(self,node,key):  # 삭제할 때 (key,value) 쌍으로 집어넣기
        if len(node.keys) == 0: # 노드에 아무것도 없으면 끝내기
            return
        
        i=self.location(node,key) # 인덱스 계산
 
        if node.keys[i-1] == key : # 해당 위치가 key 값이면 
            if node.childs ==[] : # 리프노드
                del node.keys[i-1]
            elif len(node.childs[i].keys) > self.min_key: # 내부 노드, successor
                new = self.successor(node.childs[i],key)
                node.keys[i-1] = new
                self.delete(node.childs[i],new)
            elif len(node.childs[i-1].keys) > self.min_key : # 내부노드, predecessor
                new = self.predecessor(node.childs[i-1],key)
                node.keys[i-1] = new
                self.delete(node.childs[i-1],new)
            else: # 내부노드, 왼쪽, 오른쪽 모두 최소 키 일때,
                self.merge(node,i-1) 
                # 루프노드 연결 끊기면 매꿔주기
                if node == self.root and len(node.childs) == 1:
                    self.root = node.childs[0]
                    self.delete(self.root, key)
                else:
                    self.delete(node,key)
        else: # 해당 위치가 key 값이 아닐 경우
            if node.childs == []: 
                if key in [j for j in node.keys]:
                    index = [j for j in node.keys].index(key)
                    node.keys.pop(index)
                else:
                    pass         
            elif len(node.childs[i].keys) > self.min_key: # 자식이 최소 키 개수 이상이면 내려가기
                self.delete(node.childs[i],key)
            else:
                if len(node.childs[i-1].keys) > self.min_key and i>0: # 왼쪽이 최소 키 개수 이상이면 (이미 맨 왼쪽이었으면 오른쪽 애 중 가장 큰 값을 부모로 대체해야함)
                    self.get_left(node,i) # 왼쪽 애 중 가장 큰 거를 부모로
                    self.delete(node.childs[i],key)
                elif i+1 < len(node.childs) and len(node.childs[i+1].keys) > self.min_key: # 오른쪽이 최소 키 개수 이상이면 (이미 맨 오른쪽이면 그 보다 오른쪽 없으니까 오류 생김)
                    self.get_right(node,i) # 오른쪽 애 중 가장 작은 거를 부모로
                    self.delete(node.childs[i],key)
                else: # 왼쪽 오른쪽 둘다 최소 키 개수면 
                    if i > 0 : 
                        self.merge(node,i-1)
                    else :
                        self.merge(node,i)
                    if node == self.root and len(node.childs) == 1:# 루트 노드 뭉개지면 다시
                        self.root = node.childs[0]
                        self.delete(self.root,key)
                    else:
                        self.delete(node,key)
    
    
    def successor(self,node,key): # 오른쪽 트리 중 가장 작은 값
        if node.childs ==[]:
            return node.keys[0]
        else:
            return self.successor(node.childs[0],key)
    def predecessor(self,node,key): # 왼쪽 트리 중 가장 큰 값
        if node.childs ==[]:
            return node.keys[-1]
        else:
            return self.predecessor(node.childs[-1],key)
    
    def get_left(self,node,i): # 왼쪽 중 큰 값을 부모로 대체
        node.childs[i].keys = [node.keys[i-1]] + node.childs[i].keys
        if node.childs[i].childs != []: # 자식이 있으면 자식도 데려오기
            node.childs[i].childs = [node.childs[i-1].childs[-1]] + node.childs[i].childs
        node.keys[i-1] = node.childs[i-1].keys[-1]

        del node.childs[i-1].keys[-1]
        if node.childs[i].childs != []:
            del node.childs[i-1].childs[-1]
    
    def get_right(self,node,i): # 오른쪽 중 작은 값을 부모로 대체
        node.childs[i].keys = node.childs[i].keys + [node.keys[i]]
        if node.childs[i+1].childs != []: # 자식이 있으면 자식도 데려오기
            node.childs[i].childs = node.childs[i].childs + [node.childs[i+1].childs[0]]
        node.keys[i] = node.childs[i+1].keys[0]
        
        del node.childs[i+1].keys[0]
        if node.childs[i+1].childs != [] :
            del node.childs[i+1].childs[0] 
    
    def merge(self,node,i): # 양쪽 자식 병합
        new = Node([],[]) # 새로운 노드 만들기
        new.keys = node.childs[i].keys + [node.keys[i]] + node.childs[i+1].keys
        new.childs = node.childs[i].childs + node.childs[i+1].childs
        del node.keys[i]
        del node.childs[i:i+2]
        node.childs = node.childs + [new]
        node.childs.sort()
        

        
def main():
    tree=Tree(6)
    key_find = []
    value_find = []
    key_find2 = []
    value_find2 = []
    score = 0
    score2 = 0
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
                key,value = tree.search_key(input_key[i],tree.root)
                key_find.append(key)
                value_find.append(value)
                score += (key_find[i] == input_key[i]) & (value_find[i] == input_value[i])
            compare=pd.DataFrame([key_find,value_find]).T
            compare.to_csv('input_compare.csv',header=False,index=False,sep='\t')
            print('총 {0}개 중 {1}개를 맞췄습니다. 점수는 100점 중 {2}점 입니다.'.format(len(input_key),score,(score*100)/len(input_key)))
            answer=int(input('원하는 입력을 입력하세요. : 1. insert 2. delete  3. quit\n'))
                
        if answer == 2:
            file2=input('파일 이름을 입력하세요. (확장자 명 포함)\t')
            data2 = pd.read_csv(file2,header=None,sep='\t')
            delete_key = data2.iloc[:,0].values.tolist()
            delete_value = data2.iloc[:,1].values.tolist()
            data3 = pd.read_csv('delete_compare.csv',header=None,sep='\t')
            compare_key = data3.iloc[:,0].values.tolist()
            compare_value = data3.iloc[:,1].values.tolist()
            
            print('삭제를 시작합니다.')
            for i in tqdm(range(data2.shape[0])):
                tree.delete(tree.root,(delete_key[i],delete_value[i]))
            print('삭제가 완료되었습니다.')
            
            print('검색을 시작합니다.')
            for i in tqdm(range(data3.shape[0])):
                key,value = tree.search_key(compare_key[i],tree.root)
                key_find2.append(key)
                value_find2.append(value)
            compare2 = pd.DataFrame([key_find2,value_find2]).T
            compare2.to_csv('input_delete.csv',header=False,index=False,sep='\t')
            data4 = pd.read_csv('input_delete.csv',header=None,sep='\t')
            final_key = data4.iloc[:,0].values.tolist()
            final_value = data4.iloc[:,1].values.tolist()
            for i in range(len(final_key)):   
                score2 += (int(final_key[i]) == int(compare_key[i])) & (str(final_value[i]) == str(compare_value[i]))
        
        
            print('총 {0}개 중 {1}개를 맞췄습니다. 점수는 100점 중 {2}점 입니다.'.format(len(compare_key),score2,(score2*100)/len(compare_key)))
            answer=int(input('원하는 입력을 입력하세요. : 1. insert 2. delete  3. quit\n'))

if __name__ == '__main__':
    main()      