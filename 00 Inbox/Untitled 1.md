See if there's any way to save a partial planning session so that we're not duplicating work and wasting tokens 

Need to define the tools used for GitHub. Hopefully we can just use raw API calls using curl and the GH commands token. 

Do we also need to store any date, time information or anything that would help us understand if an issue has been updated. We don't want to pull down issues and reevaluate the whole thing if nothing's changed on the issue itself. 

Is it possible to use a heartbeat to check for issue changes without using the llm at all. So wake up make an API call based on some saved timestamp and if there's things in it then use the llm. 

I'd like to make a decisions.md file where we can record important decisions that we can use as input to future design.

Add some local configuration to limit the total number of API calls or the total cost or maybe even the total number of tokens created. 

