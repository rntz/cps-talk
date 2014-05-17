module Regexp where

data Re
    -- character literals
    = Lit Char
    -- (Seq a b) is concatenation /ab/
    | Seq Re Re
    -- (Or a b) is choice /a|b/
    | Or Re Re
    -- (Star a) is iteration /a*/
    | Star Re
      deriving (Show, Eq)

match :: Re -> String -> (String -> Bool) -> Bool
match (Lit c) [] k = False      -- a literal doesn't match the empty string!
match (Lit c) (x:xs) k =
    if c == x                   -- if the first character matches,
    then k xs                   -- try matching the rest of the string
    else False                  -- (if it didn't, we're screwed)

match (Seq a b) s k =
    match a s                       -- match a...
          (\rest -> match b rest k) -- then match b
-- Note how we modified our continuation - we added more work to do!

match (Or a b) s k =
    match a s k                 -- try matching a...
    || match b s k              -- else try b
-- Note how we might call our continuation twice - backtracking!

match (Star a) s k =
    -- one or more case, /aa*/
    match a s (\rest -> match (Star a) rest k)
    -- empty case, //
    || k s

matches :: Re -> String -> Bool
matches a s = match a s null
-- We pass null because we want to match the *whole* string - so the "work left
-- to do" is to check that there's nothing left in the string, which is what
-- null does.

-- A more concise implementation.
match2 :: Re -> String -> (String -> Bool) -> Bool
match2 (Lit c) [] k = False
match2 (Lit c) (x:xs) k = c == x && k xs
match2 (Seq a b) s k = match2 a s (\rest -> match2 b rest k)
match2 (Or a b) s k = match2 a s k || match2 b s k
match2 (Star a) s k = match2 a s (\rest -> match2 (Star a) rest k) || k s
