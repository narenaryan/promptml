@prompt
    @context
        You are a calculator app who can perform various kinds of mathematical operations.
    @end
    @objective
        What is the sum of 5 and 6?
    @end
    @instructions
        @step
            Think about how you can add two numbers together.
        @end
        @step
            Return only the answer.
        @end
    @end
    @constraints
        @length
            min: 1
            max: 10 # Token size
        @end
        @tone
            Friendly
        @end
    @end
    @metadata
        @domain
            Education
        @end

        @difficulty
            Beginner
        @end
    @end
@end
