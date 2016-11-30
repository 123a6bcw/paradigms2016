module Main where

import Prelude hiding(lookup)

data BinaryTree k v = None | Node {
    key :: k,
    value :: v,
    left :: BinaryTree k v,
    right :: BinaryTree k v
} deriving (Eq)

walking k1 k2 a b c = if k1 < k2 
                      then
                             a
                      else
                              if k1 == k2
                              then
                                      b
                              else
                                      c

lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup key' None = Nothing
lookup key' node = walking key' (key node)
                   (lookup key' (left node))
                   (Just(value node))
                   (lookup key' (right node))

insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert key' value' None = Node key' value' None None
insert key' value' node = walking key' (key node) 
                          (Node (key node) (value node) (insert key' value' (left node)) (right node))
                          (Node key' value' (left (merge (left node) (right node))) (right (merge (left node) (right node))))
                          (Node (key node) (value node) (left node) (insert key' value' (right node)))

delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete key' None = None
delete key' node = walking key' (key node)
                   (Node (key node) (value node) (delete key' (left node)) (right node))
                   (merge (left node) (right node))
                   (Node (key node) (value node) (left node) (delete key' (right node)))

merge :: BinaryTree k v -> BinaryTree k v -> BinaryTree k v
merge None b = b
merge a None = a
merge a b = Node (key b) (value b) (merge a (left b)) (right b)

main = do
    print (lookup 5 (insert 1 1 (insert 13 12 (insert 9 10 (insert 5 19 None)))))
    print (lookup 5 (delete 13 (insert 1 1 (insert 13 12 (insert 9 10 (insert 5 19 None))))))
    print (lookup 1 (insert 1 4 (insert 13 12 (insert 9 10 (insert 5 19 None)))))
    print (lookup 1 (delete 1 (insert 1 4 (insert 13 12 (insert 9 10 (insert 5 19 None))))))
    print (lookup 1 (insert 1  10 (insert 1 1 (insert 13 12 (insert 9 10 (insert 5 19 None))))))
