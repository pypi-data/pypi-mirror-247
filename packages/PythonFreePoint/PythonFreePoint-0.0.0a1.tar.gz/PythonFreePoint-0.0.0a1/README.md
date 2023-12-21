# Point Free Style for Python

## Introduction: 

This is a minimal Python3 library that provides you with tools to work in Python as-if the language had point-free 
style, similar to how something like BASH would operate.

    @pointfree()
    def foo(point):
        return point + 1


    @pointfree()
    def bar(point):
        return point * 8

    print( foo + bar << 2 )

    > RETURNS '24'

## What's the point?

Inspired by talks about point free style (in particular [this talk](https://www.youtube.com/watch?v=NcUJnmBqHTY)), 
wanted to see if a syntax "point free style" could be integrated `seamlessly` into Python3. Exactly what defines 
something as being seamless is somewhat subjective, so it shouldn't be seen as written in stone.

Instead, the idea is that the piping of functions should be quick and painless, with the user knowing if they are 
working with something that captures multiple inputs or a single one. When working with layered level of inputs, the 
functions should also take care of the piping behind the scene.

**Example:**

    print( foo + bar << [ 1, 2 , 3 ] )
    
    > RETURNS [ '16', '24', '32 ]

We can also add functions that receive ranges or return ranges.

    @pointfree()
    def into_range(point):
        return [p for p in range(point)]


    @pointfree(uses_multiple_values=True)
    def compress(points):
        return sum(points)

And the combines them into different results


    print( foo + bar + compress << [ 1, 2 , 3 ] )
    
    > RETURNS '72'

    print(foo + bar + into_range << 1 )

    > RETURNS '[ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 ]'

    print(foo + bar + into_range + compress << 1 )

    > RETURNS '120'

Disclaimer: Had to really fight the urges the claim that *"it has no point, it is point free after all"*

## MISC

### What happens if I want to add a function that also take other values?

That is actually allowed on the current code. The function will only take the first value as the replacement for the 
current point, so it is possible to define oher values later.

    @pointfree()
    def multiply_by(point,x):
        return point * x

    print(foo + multiply_by(x=2) << 1 )

    > RETURNS '4'    

### Are there other alternatives to this?

Yes, there are other Python implementations of PointFree. Some of them are probably better than thi one, although I 
intentionally avoided looking at them, since I wanted to come up with my own solutions.
