# Unsupported features in Python Tutor

[Python Tutor](http://pythontutor.com/) currently does **NOT** support the following language features. Some of these features will eventually be supported, but others probably won't, due to implementation challenges and other priorities.

Email philip@pgbovine.net with more bug reports and use the "Generate shortened link" button to include a URL so that I can reproduce them.

For more details on project status and issue prioritization, check out these videos from March 2018:
- [Python Tutor project status - 1 of 2 - common feature requests & feasible fixes](https://www.youtube.com/watch?v=oKIqejkxqP0)
- [Python Tutor project status - 2 of 2 - bigger feature requests & unlikely fixes](https://www.youtube.com/watch?v=8o-XeFTgD40)

... and this earlier video from Oct 2017: [Python Tutor Software Development Philosophy](https://www.youtube.com/watch?v=sVtXLdBRfyE)

### C and C++

- unions
- some complex typedefs
- taking text input from the user using scanf(), cin >>, etc.
- code with memory-related errors: it will fail-fast using [Valgrind
  Memcheck](http://valgrind.org/docs/manual/mc-manual.html)
- [doesn't show when function parameters get mutated](https://github.com/pgbovine/opt-cpp-backend/issues/57)
- [function return values are not visualized](https://github.com/pgbovine/opt-cpp-backend/issues/4)
- [stack arrays without compile-time sizes](https://github.com/pgbovine/opt-cpp-backend/issues/44)
- [read-only memory isn't visualized separately from the heap](https://github.com/pgbovine/opt-cpp-backend/issues/70)

### JavaScript

- asynchronous event-driven code
  - including setTimeout, setInterval, etc.
  - promises, async/await
- anything that operates on webpages, such as DOM manipulation, alert(), prompt(), confirm(), etc.
- Date() object


### Python

- some infinite loops: the server times out without showing partial results or good error messages
  - to cut down execution times, [set Python breakpoints](https://youtu.be/80ztTXP90Vs?t=42) using `#break` comments
- asynchronous code
- random number generators and user input (via input() or raw_input()) [sometimes don't work well together](https://github.com/pgbovine/OnlinePythonTutor/issues/110)
- you can't rely on the behavior of id() matching CPython; note that when teaching beginners, you shouldn't rely on id() since oftentimes these behaviors aren't part of the Python language spec (they're due to implementation-specific optimizations).
- no 3rd-party library/module support: use the experimental "Python 3.6 with <a href="https://docs.anaconda.com/anaconda/">Anaconda</a>" mode if you want to import many more modules from the Anaconda distribution
- (note: remember that Python 2 and 3 support slightly different kinds of language constructs)


### Other unsupported features (language-agnostic)

- Stepping *within* a line of code to show how subexpressions get evaluated within that line
- Unicode doesn't work well in general (especially for Ruby and Python 2); use ASCII characters when possible
- Passing in command-line arguments via argv[] array
- Multi-threaded, concurrent, or asynchronous code
- Anything involving GUI programming or GUI/webpage components
- Reading data from external files; put all your data in strings when possible
- Interfacing with databases, network, filesystem, or other external resources
- Importing external 3rd-party libraries (try "Python 3.6 with Anaconda (experimental)" if you want to use more libraries)
- Code that is too large in size; shorten your code!
- Code that runs for too many steps (e.g., > 1,000 steps) or for a long time
  - shorten your code to isolate where you want to visualize and debug
  - or [set Python breakpoints](https://youtu.be/80ztTXP90Vs?t=42) using `#break` comments
- If you're behind some kinds of firewalls or proxy servers, the visualizer may not work


Look through these issue trackers for additional bugs and unsupported features:
- https://github.com/pgbovine/OnlinePythonTutor/issues
- https://github.com/pgbovine/opt-cpp-backend/issues
