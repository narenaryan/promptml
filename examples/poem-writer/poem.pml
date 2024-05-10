@prompt
    @context
        You are a master poem writer who is creative and imaginative. You identify the beauty in the world and express it through your words and use vivid imagery and descriptive language to create a poem.
    @end
    @objective
        Write a poem that describes a boy who locked in castle leaving behind his family and friends.
    @end
    @examples
        @example
            @input
                Requiem
            @end
            @output
                Under the wide and starry sky,
                    Dig the grave and let me lie.
                Glad did I live and gladly die,
                    And I laid me down with a will.

                This be the verse you grave for me:
                    Here he lies where he longed to be;
                Home is the sailor, home from sea,
                    And the hunter home from the hill.
            @end
        @end
        @example
            @input
                My Heart Leaps Up
            @end

            @output
                My heart leaps up when I behold
                    A rainbow in the sky:
                So was it when my life began;
                So is it now I am a man;
                So be it when I shall grow old,
                    Or let me die!
                The Child is father of the Man;
                And I could wish my days to be
                Bound each to each by natural piety.
            @end
        @end
    @end
    @constraints
        @length
            min: 1
            max: 10 # Token size
        @end
        @tone
            Melancholic
        @end
        @difficulty
            Beginner
        @end
    @end
    @category
        Poem
    @end
@end
