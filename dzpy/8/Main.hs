module Main where

head' :: [a] -> a
head' (x:xs) = x

tail' :: [a] -> [a]
tail' [] = []
tail' (x:xs) = xs

take' :: Int -> [a] -> [a]
take' 0 xs = []
take' n [] = []
take' n (x:xs) = x:take' (n - 1) xs

drop' :: Int -> [a] -> [a]
drop' 0 xs = xs
drop' n [] = []
drop' n (x:xs) = drop' (n - 1) xs

filter' :: (a -> Bool) -> [a] -> [a]
filter' f [] = []
filter' f (x:xs) =
                    if f x
                    then
                        x:filter' f xs
                    else
                        filter' f xs

foldl' :: (a -> b -> a) -> a -> [b] -> a
foldl' f z [] = z
foldl' f z (x:xs) = foldl' f (f z x) xs

concat' :: [a] -> [a] -> [a]
concat' [] a = a
concat' a [] = a
concat' (x:xs) a = x : (concat' xs a)

quickSort' :: Ord a => [a] -> [a]
quickSort' [] = []
quickSort' (x:xs) = concat' (concat' (quickSort' (filter' (< x) xs)) [x]) (quickSort' (filter' (>= x) xs))
