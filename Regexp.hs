module Regexp where

data Regexp
    = Char Char                 -- literal character
    -- (Seq a b) represents concatenation /ab/
    | Seq Regexp Regexp
    -- (Or a b) represents choice /a|b/
    | Or Regexp Regexp
    -- (Star a) represents iteration /a*/
    | Star Regexp
      deriving (Show, Eq)

match :: Regexp -> String -> (String -> Bool) -> Bool
match (Char c) [] k = False
match (Char c) (x:xs) k =
    if c == x
    then k xs
    else False
match (Seq a b) s k =
    match a s                       -- match a...
          (\rest -> match b rest k) -- and then match b on the rest
match (Or a b) s k =
    match a s k                 -- try matching a...
    || match b s k              -- or else try b
match (Star a) s k =
    match a s (\rest -> match (Star a) rest k) -- one or more case
    || k s                                     -- empty case

matches :: Regexp -> String -> Bool
matches a s = match a s null
