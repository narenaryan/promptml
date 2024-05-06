# Define prompt variables
@vars
    role = 'highly skilled and experienced software developer'
@end

# Define prompt
@prompt
  # Context is used to provide background information or context for the task
  @context
      You are a $role with expertise in various programming languages and frameworks. You have been tasked with creating a new web application for a social media platform.
  @end

  # Objective is used to define the main goal or objective of the task
  @objective
      Design and implement the core architecture and components for a scalable and efficient web application that can handle a large number of concurrent users while providing a seamless and responsive user experience.
  @end

  # Instructions are used to provide detailed steps or guidelines for completing the task
  @instructions
      # steps can be used to break down the task into smaller parts
      @step
          Identify the key features and requirements of the web application based on the provided context.
      @end
      @step
          Propose a suitable architecture (e.g., monolithic, microservices, etc.) and justify your choice.
      @end
      @step
          Outline the essential components or modules of the application, such as user authentication, data storage, real-time communication, and so on.
      @end
      @step
          Discuss the potential technologies, frameworks, and tools you would use to implement each component, highlighting their strengths and trade-offs.
      @end
      @step
          Address scalability and performance concerns, including techniques for load balancing, caching, and database optimization.
      @end
      @step
          Describe how you would ensure the security and privacy of user data, including authentication, authorization, and data encryption.
      @end
  @end

  # Examples are used to provide sample inputs and outputs for the task
  @examples
      @example
          @input
              Design the core architecture and components for a large-scale e-commerce web application.
          @end
          @output
              For a large-scale e-commerce web application, a microservices architecture would be suitable due to its inherent scalability and flexibility...
          @end
      @end
      @example
          @input
              Outline main components for a large-scale e-commerce web application.
          @end
          @output
              Product Catalog, User Management, Order Processing, Payment Gateway, Search Engine, Recommendation Engine are the main components of a large-scale e-commerce web application...
          @end
      @end
  @end

  # Constraints are used to specify any limitations or restrictions for the task
  @constraints
      @length
          min: 1000
          max: 3000
      @end
      @tone
          Professional and technical
      @end
      @difficulty
          Advanced
      @end
  @end

  # categories are used to classify the task into different categories
  @category
      Software Engineering
  @end

  # Metadata includes information such as domain, difficulty, custom props, etc.
  @metadata
      top_p: 0.6
      temperature: 0.5
      n: 1
      internal: 'true'
  @end
@end
