
I was really impressed with the new direction of the business college. It's interesting because it aligns directly with how I got into my industry in my experience, where it's more about the experience that you bring to the organization than it is about the degree by itself.

I have this idea I wanted to run by you. I've been working on this class for applying agentic workflows to different types of processes. The class isn't really designed for case, necessarily. I was looking to start publishing courses on this topic separately, but today's meeting really got me thinking about how this could be applied to the future of the program.

The concepts are really not technical in nature. I don't want to go over how LLMs work or graph theory or anything like that. What it really is, is an extension to my current class: take logical thinking and create structured documentation for a process, a business process, a coding workflow, or things like that, in such a way that an agentic agent infrastructure could take it and actually execute on it. I was thinking about not know how to apply it to things like bug triaging or security vulnerability, triaging but other business processes like ??.

I think something like this really aligns well with the future program., especially when it's taught to individuals that are in the master's program that I already have industry experience. We really allow them to leverage AI technologies and apply them to the domain where they're already an expert, and increase their productivity. Was thinking something something similar to 
https://execonline.cs.cmu.edu/agentic-ai-program but with more of a practical, Hands-On non-technical focus. Essentially, it's kind of a next step to my current course. In my current course is really logic and reasoning at a highly technical level and this really applies that logic and reasoning to automating a process using AI. Trying to keep things very light on the code by choosing the framework and infrastructure that could be used to build most things and not have to have a significant amount of technology background. 

In my current course, logic and reasoning are really at a highly technical level, and this really applies that logic and reasoning to automating a process using AI. The big difference is there's no code. Trying to keep things very light on the code by choosing the framework and infrastructure that could be used to build most things and not have to have a significant amount of technology background. I'd be interested in hearing your thoughts on this, both from a practicality standpoint and if it might be something useful to the business school in general.

---

Hi [Dean's Name],

I really enjoyed today's discussion about the direction of the business school. One aspect that particularly resonated with me was the emphasis on practical experience. In many ways, it reflects my own path into the industry, where the value someone brings is often determined as much by the experience and problem-solving ability they bring to an organization as by the degree itself.

The meeting also sparked an idea that I'd like to get your thoughts on.

I've been developing a course around designing AI-enabled workflows (often referred to as agentic AI or agentic workflows) for real-world business processes. Originally, I intended to offer it independently, but after today's discussion, I began to see how well it might fit within the future direction of the business school.

Despite the topic, the course is not primarily about AI technology. It doesn't focus on how large language models work, graph theory, or machine learning. Instead, it's about teaching students how to analyze complex processes, document them in a structured way, and design workflows that AI agents can execute reliably alongside human experts.

In many ways, I see it as a natural extension of the Python course I currently teach. That course develops logical reasoning and structured problem solving through programming. This course would apply those same reasoning skills to designing AI-assisted workflows—with little to no programming required.

The emphasis would be on practical applications across many domains. Examples might include software development workflows such as bug triage, security vulnerability management, customer support, document review, compliance processes, project management, financial operations, procurement, HR onboarding, and other business processes where well-defined procedures can be augmented by AI.

What excites me most is that this could be especially valuable for master's students who already have industry experience. Rather than teaching them a new profession, the course would help them apply AI within domains where they are already experts, enabling them to improve productivity, automate repetitive work, and rethink existing business processes.

Conceptually, I envision something similar to Carnegie Mellon's executive program on agentic AI, but with a much more practical, hands-on, and non-technical focus. Rather than teaching students how to build AI models, the goal would be to teach them how to analyze, design, and implement AI-enabled workflows using existing frameworks and tools.

I'd be very interested in hearing your thoughts on whether a course like this seems practical and whether you think it could complement the broader direction of the business school.

Thanks again for the discussion today. It definitely gave me a lot to think about.

---

Hi [Dean's Name],

I really enjoyed yesterday's discussion about the direction of the business school. One aspect that particularly resonated with me was the emphasis on practical experience. In many ways, it reflects my own path into the industry, where the value someone brings is more often determined by the experience and problem-solving ability they bring to an organization than by the degree itself.

The meeting also sparked an idea that I'd like to get your thoughts on.

I've been developing a course around designing AI-enabled workflows (often referred to as _agentic AI_ or _agentic workflows_) for real-world business processes. Originally, I intended to offer it independently, but after today's discussion, I began to see how well it might fit within the future direction of the business school.

Despite the topic, the course is not primarily about AI technology. It doesn't focus on how large language models work, graph theory, or machine learning. Instead, it's about teaching students how to analyze complex processes, document them in a structured way, and design workflows where AI agents and people work together effectively, with appropriate human oversight.

In many ways, I see it as a natural extension of the Python course I currently teach. That course develops logical reasoning and structured problem solving through programming. This course would apply those same reasoning skills to designing AI-assisted workflows—with little to no programming required.

The emphasis would be on practical applications across many domains. Students would learn to decompose complex work into repeatable processes and create the structured documentation needed for AI systems to execute portions of those workflows. Examples might include software development processes such as bug triage and security vulnerability management, as well as customer support, document review, compliance, project management, procurement, HR onboarding, and other business functions where AI can meaningfully augment human expertise.

What excites me most is that this could be especially valuable for master's students who already have industry experience. Rather than teaching them a new profession, the course would help them apply AI within domains where they are already experts, enabling them to improve productivity, automate repetitive work, and rethink existing business processes.

Conceptually, I envision something similar to Carnegie Mellon's executive program on agentic AI, but with a much more practical, hands-on, and non-technical focus. Rather than teaching students how to build AI models, the goal would be to teach them how to analyze, design, evaluate, and iteratively improve AI-enabled workflows using existing frameworks and tools. The emphasis would be on applying sound reasoning and process design—not on software engineering.

I'd be very interested in hearing your thoughts on whether a course like this seems practical and whether you think it could complement the broader direction of the business school.

Thanks again for the discussion yesterday. It definitely gave me a lot to think about.


---
I can work on distilling what I currently have into a syllabus. Some of my plans may need a little redirection since I was originally envisioning this as a bootcamp-style course.

There are a few design considerations we’ll need to address for a university setting:

1. LLM access. My original plan was to expose a token-throttled LLM through a custom harness while also allowing students to bring their own API keys if they preferred.
2. Cost management. Keeping AI usage predictable for both the university and students.
3. Student hardware/software consistency. Ensuring everyone has access to the same tooling and development environment.
4. Corporate partnerships. I think this could be a really interesting opportunity, particularly toward the end of the semester.

One challenge with incorporating industry partners is that the first part of the course is intentionally structured. Early in the semester, each class introduces a single business process along with one or two new AI integration techniques. Every exercise builds on the previous ones, so the workflows need to be tightly controlled. For example, if we’re teaching an intake request workflow, I’d simulate the business by providing a mix of hardcoded and AI-generated requests. The processes are deliberately chosen because they’re familiar business workflows that isolate the specific concepts we’re teaching without introducing unnecessary complexity.

Toward the end of the semester, however, I think a corporate partnership could fit very well. By that point, students would have a solid foundation in process decomposition, AI-assisted workflow design, and governance. They could then apply those skills to a real business process supplied by an industry partner, giving them experience with authentic ambiguity while also providing value to the organization.