# Scenes — AI English Learning Environment

> **Status:** Incubating  
> **Role:** AI Native Product Lab / secondary project  
> **Current priority:** Keep the idea alive and validate the product hypothesis; do not let it displace the current AI Agent main project.

## 1. One-line idea

**Turn familiar real-world scenes into an English-only learning environment, so learners build a direct connection between the world, meaning, and English instead of relying on Chinese translation.**

Working product line:

> **Learn English from the world around you.**

Long-term direction:

> **Turn your world into English.**

---

## 2. Core learning belief

Traditional vocabulary learning often trains this path:

`English -> Chinese -> meaning`

Scenes wants to strengthen:

`real scene / image / action -> English -> meaning -> expression`

The product should therefore avoid treating Chinese translation as the default learning interface. Images, objects, actions, sounds, definitions, examples, and conversations should provide enough context for users to infer meaning directly in English.

The goal is not simply to increase vocabulary count, but to gradually make English part of the user's perception of everyday life.

---

## 3. Target user

Initial target:

- Chinese learners who already have basic English knowledge but still mentally translate too much.
- Learners who want practical, everyday English rather than exam-oriented vocabulary lists.
- Learners who prefer visual, contextual, immersive learning.
- Learners who want to become comfortable thinking and communicating directly in English.

This product is probably **not** primarily designed for complete beginners who still need extensive bilingual scaffolding.

---

## 4. Core product loop

### Free loop — Fixed World

`choose a scene -> explore objects/actions -> understand through image + English -> recall -> review`

Example scenes:

- Home
- Café
- Campus
- Work
- Shopping
- Restaurant
- Airport
- Travel

A scene should feel like a place to explore, not a vocabulary list.

### Premium loop — Personal World

`take a photo -> AI understands the scene -> generate an English environment -> explore -> talk in context -> save useful language -> review later`

The key premium value is **personal context**, not generic AI chat.

---

## 5. Free version

The free product must be useful even without AI.

### Fixed scenes

Each scene contains:

- a strong visual scene
- interactive objects
- useful actions and verbs
- English-only definitions
- pronunciation/audio
- natural example sentences
- common expressions connected to the scene

### Vocabulary memory

Prefer a richer learning state than `learned = true`:

`unknown -> familiar -> recognizable -> retrievable -> usable`

Review should emphasize image/meaning -> English recall rather than English -> Chinese translation.

Possible first MVP scenes:

1. Home
2. Café
3. Campus

Keep content deliberately small at first: roughly 20–30 useful concepts per scene rather than hundreds of isolated words.

---

## 6. Paid / subscription version

### 6.1 Capture a Scene

The user photographs a real environment, such as a bedroom, desk, café, supermarket, classroom, or street.

AI extracts structured information such as:

- scene type
- visible objects
- possible actions
- useful expressions
- relationships between objects

The result should feel like:

> **This is your world in English.**

### 6.2 Contextual AI Conversation

Conversation should always have a meaningful context.

Example:

`photo of a café -> ordering scenario -> user speaks -> AI continues the situation -> lightweight correction when useful`

Avoid becoming a generic "chat with an English tutor" interface.

AI should primarily act as a **conversation partner inside the scene**, and only secondarily as a teacher.

### 6.3 Personal English World

Over time, the system can accumulate a user's scenes, concepts, expressions, weak points, and successful usage.

Possible long-term model:

`Scene -> Concept -> Expression -> Experience`

This can gradually become a personal **English World Model** rather than a traditional vocabulary database.

---

## 7. AI Native principle

AI is not the product by itself.

The product should remain:

`learning philosophy + interaction design + user data loop + AI capability`

For AI-generated content, prefer:

`multimodal model -> structured output -> validation -> domain model -> UI`

Do not let raw LLM output directly control the product experience.

Potential AI capabilities:

- multimodal scene understanding
- contextual vocabulary generation
- personalized difficulty selection
- scene-based conversation
- meaningful correction
- review generation from previous real experiences

---

## 8. Business model hypothesis

### Free

- fixed scenes
- image-English vocabulary learning
- pronunciation
- basic review
- progress tracking

### Premium

- photo-to-scene generation
- AI contextual conversation
- saved personal scenes
- personalized language generation
- deeper review based on personal learning history

The paywall should separate **fixed public worlds** from **your own AI-generated world**.

---

## 9. Why this project matters

This project can eventually serve as a practical AI Native Builder project because it combines:

- iOS / SwiftUI
- product and interaction design
- backend engineering
- multimodal models
- AI reliability and structured outputs
- learning-system design
- subscription/product economics
- real-user feedback

It is a good application layer for Agent / AI engineering knowledge developed elsewhere.

---

## 10. Why it stays in the incubator for now

The current AI Agent project has higher short-term learning leverage for understanding:

- agent architecture
- state and memory
- evaluation
- observability
- failure analysis
- tool use
- reliability

Scenes should therefore remain a secondary product experiment rather than becoming the main engineering project immediately.

A reasonable near-term allocation is roughly:

`AI Agent main project 80% / Scenes incubation 20%`

For Scenes, the incubation phase should focus on product definition, UX prototypes, and a tiny fixed-scene SwiftUI prototype rather than building the full AI stack.

---

## 11. Promotion criteria: Incubator -> Real Project

Promote Scenes into an active standalone project when most of these are true:

- the current Agent system has a complete working loop
- basic structured logging / observability exists
- there is a usable evaluation mechanism
- failure modes can be classified and explained
- the Agent system has been tested by real users
- the Scenes core loop still feels compelling after prototype testing
- at least a few target users understand when and why they would open Scenes

At that point, Scenes can become the product layer where the accumulated AI engineering capabilities are applied to a real consumer experience.

---

## 12. First incubation task

Do **not** build the full app yet.

Create one tiny prototype that answers one question:

> **Does exploring a familiar visual scene with English-only labels, definitions, audio, and recall feel more natural and useful than learning the same words from a traditional vocabulary list?**

Suggested prototype:

- 3 fixed scenes: Home / Café / Campus
- 20–30 concepts per scene
- image + English only
- tap-to-explore interaction
- pronunciation
- one lightweight recall loop

The next decision should be based on actual use, not feature imagination.

---

## 13. Open questions

- What exact learner level benefits most from English-only contextual learning?
- How much ambiguity can images resolve without translation?
- What should make users return every day?
- What is the smallest effective review loop?
- When is correction helpful versus disruptive?
- How much AI personalization creates real learning value rather than novelty?
- Is photo-to-scene compelling enough to support subscription retention after the novelty wears off?

These questions should be validated before expanding scope.
