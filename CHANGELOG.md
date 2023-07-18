# Change Logs

### v0.2.0 - Conversation ID (BC)
- Add 'cid' to ConversationHistory to make conversations query separable
- Enhance the save method on Persistence to board 'cid'
- Enhance the find method on Persistence to board 'cid'
- Fix on empty function calls for OpenAIChat
- Minor Bug Fixing

### v0.1.14 - Automatic Character Building
- Added AutoPersonnel class to auto build characters using GPT Complete.
- Added save_json method on BasePersonnel to save the personnel's data as a JSON
- Added OpenAIComplete for GPT Generate and Complete method
- Minor Bug Fixes

### v0.1.12 - Split Dependencies to Extras
- Added extra packaging for 'database' and 'function'
- Added more characters (Claude Monet, Pablo Picasso, and Van Gogh)
- Minor Bug Fixes

### v0.1.8 - Added Postgres and MySQL Persistence
- Added Postgres Persistence
- Added MySQL Persistence
- Added Unit Test for Persistence
- Revise Unit Test for Interface
- Minor Bug Fixes

### v0.1.7 - Added Persistence Clear and Error Management
- Added 'clear' method for BasePersistence
- Added 'clear' method for MemoryPersistence
- Added 'clear' method for SQLitePersistence
- Added Error Management for Unfulfilled Credential
- Minor Bug Fixes

### v0.1.6 - Added WriteSonic and Bug Fixes
- Added WriteSonic (PhotoSonic) API in Interface
- Added Unit Test for Interface
- Bug Fixing and Cleanups on Interface Classes

### v0.1.5 - Fix Dependency
- Added Project on PyPI
- Fixed Dependency Errors
- Revise README and Package Information

### v0.1.0 - First Push

- Initial Idea of the Jam Engine
- Initial Idea of the Instrument as Function Calls
- Implement Interface OpenAI as Chat Engine with Function Calls
- Implement Interface DALL-E and Stability as Image Generation Interface
- Implement PromptPainter as Image Generation Instrument
- Implement BasicPersonnel as a Starter Kit
- Implement SQLite as Persistence
- Added 4 Example Personnel (Albert Einstein, Homer Simpson, Marie Curie, and Walter White)
- Added Command Line Interface to Implement Jam