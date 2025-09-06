# Intro

---
### This 'README' is more of a collation of various notes from my Logseq files that I write during breaks from testing, whilst the project is WIP. Therefore don't expect too much coherence or fancy writing, i'll do that once its finished.

- If you're really bored you can also read my first blog (whilst my website is WIP) [here](https://github.com/David-Barnes-Data-Imaginations/blog.github.io/blob/main/_posts/2025-08-10-titles.md).

---
**For Clinicians / Non-Techies**:
- I present the core 'Psychology principles' involved first, to spare the pain of technical jargon. I cover _some_ technical aspects related to 'Knowledge Graphs', but graph syntax is closer to 'Structured English' than it is to a 'Coding Language'.
- The concept was developed from a [project](https://github.com/David-Barnes-Data-Imaginations/SentimentSuite) that was intended to be a 'light demo' for a friend, using 'Russells Cicumplex' and 'utterances' to evaluate therapy session transcripts (Carl & Gloria etc.)
---
**For 'Techies' or those learning to build 'Advanced Agentic Systems'**: 
- At the very bottom is the 'Safety & Ethics' section, outlining how to run experiments with the incredibly powerful 'Smolagents' library, in a safe dev environment. This also contains advice on _how to learn_ 'SmolAgents' most powerful 'CodeAgent' functionality.
- Whilst this project has a specific goal / subject, the architecture has intentionally been built to be flexible enough so that it can be easily transferrable to other domains. These might include: Housing, Information Security or general business / government organizations.

**Security**:
- All my code runs 'on its own computer' in a similar way to the online models.

### **_Why_ agentic frameworks?**
 
- Now if you're still getting to grip with the concept of agentic frameworks, who better to summarise than a former 'Google CEO' and 'Whitehouse Advisor' to multiple US Presidents: [Eric Schmidt](https://en.wikipedia.org/wiki/Eric_Schmidt).
- Bear in mind this was recorded a month ago, and a hell of a lot has happened in that month.
- The key segment is at [10:57] in this [video](https://www.youtube.com/watch?v=qaPHK1fJL5s). The process he describes in perfectly feasible, even 'easy' once you have a smolagents runner like mine.

### Here's a trimmed snippet if you want the tldr:

---
**_"The remarkable thing... and this is to me is shocking... is you can in 'an enterprise', write the task that you want and then connect your databases with an LLM which can produce the code for your enterprise.
If you built a brand new enterprise architecture, you would be highly tempted use open-source libraries, and essentially build that architecture, giving you infinite flexibility and the computer system and writes most of the code."_**

_Eric Schmidt_ July 2025

---

- ### TODO Note: After spending nearly 5 days trying to get gpt-oss to run across unified memory on Ollama, building servers for Triton, vLLM, Llama.cpp, and even a Custom Hugging Face API docker, Ollama is finally fixed on ubuntu.


# TODO's

# Project Update
The forge has been built, albeit still under testing. 

I also pivoted the whole project and re-wrote it using LangGraph, with tracing for the runs on Langsmith.

Since the project files are completely different, I haven't yet decided how I'm going to add to Github, maybe here, maybe as a seperate project.

Whilst I decide, here are some screenshots (yes that's me it's analyzing), currently being tested with the small gpt-oss for speed purposes.

I've also built a LangGraph voice assistant, which listens, transcribes and talks back.

The voice assistant will be built into my Jetson part of the project.


  <h2 align='center'>
  A basic front end til I get round
  </h2>
  <br><br>
<p align="center">
  <img src="./front-page-forge.png" alt="Front-end">
</p>

  <h2 align='center'>
  This is how you view model runs in Langsmith, though the code produces a download file with the models output
  </h2>
  <br><br>
<p align="center">
  <img src="./Langsmith_trace_viewer_3.png" alt="example 1">
</p>

  <h2 align='center'>
  The Cypher for the knowledge graph is currently lumped in with the rest. That will be extracted with another agentic parse.
  </h2>
  <br><br>
<p align="center">
  <img src="./Langsmith_trace_viewer_4.png" alt="example 2">
</p>

  <h2 align='center'>
  The agentic workflow makes the model fix its mistakes, so these error's get corrected in realtime
  </h2>
  <br><br>
<p align="center">
  <img src="./Langsmith_trace_viewer_5.png" alt="example 3">
</p>

---
>###  ⛔ Please Review and Consider Example 'Risk Register' Schema before implementing anything beyond Dev phase, found at bottom of document⛔'**.
---

# The Persona-Forge
- The Persona-Forge has been a project of mine for close to two years, 'evolving' as I have 'pivoted' towards new tech and ideas.
  > Hear the concept of 'pivoting in AI' from one of the 'Godfathers of AI' - Andrew Ng from around '7:50' [here](https://www.youtube.com/watch?v=RNJCfif1dPY).
  
- It began as a simple idea to map personalities of anything from video games, to my own persona, using 'Knowledge Graphs' to map out 'Personality Constructs', or 'Persona'. Mapping include 'speaking tone' & 'vocabulary', profiling frameworks (e.g. 'Myers Briggs', history (e.g. key events in a persons life, and the emotions they trigger) and even metaphor or common phrase types that the character uses.
- My lifelong passion for Psychology, the pace of AI, and my preference for 'altruistic projects' caused me to pivot to a more specific goal. The pivot was also inspired by the realization that it could be achieved by simply merging three of my portfolio projects and a LOT of testing.
- The _first half_ of the README is written with 'Clinicians' as the primary audience, to demo possibilities with non-technical jargon in the first half of the document.
- The _second half_ covers more technical aspects for the _art_ of AI building, Persona-mappings, or 'Using AI to _augment_ people or processes. This covers 'Hardware Considerations', 'Testing', Safety, and learning 'Agentic Frameworks'.
---

---
The Persona-Forge is designed to help therapists and mental health hospitals modernize and care for patients. I'm scoping an adaptation for criminal profiling and pattern matching, both 'online' and in the 'real-world'.

# Use Cases:

## 1. Hospital and/or Therapist/Clinician Support - 'Vision of the Future'
There are two main elements, three AI models involved, a bunch of UI/Interface tools and many hours of research:

## Elements:
- To modernize Psychology, by providing the superhuman pattern matching and profiling abilities of AI, for Therapists and Hospitals. 
- This enhances insights for better work, _benefits_ the care for patients, and help therapists learn from their own techniques. 
- It cannot be stressed enough that this does not aim to 'replace' human therapists, clinicians or their current methods. 
- 'It's 'AI - Human augmentation via fusion'. _How_ this actually functions on a 'practical' / 'daily' level is still under intense scrutiny. The reason is the same reason that I love to build AI, I do _extensive_ testing (makes up about 70% of the work), and I'm being so blown away with idea's and possibilities I hadn't percieved, simultaneaously pivoting away from others that I thought _might_ work. 
- Modernizing patient interactions to streamlined automation processes that remove pen & paper based tools, again freeing up staff resources to care for patients more effectively.

## AI Models:

### Local (stressed for importance of privacy):
- GPT-oss:20b/120b locally hosted 'multi-modal' model for: agentic workflow automation using an adaptation of my [smolagents agentic runner framework](https://github.com/David-Barnes-Data-Imaginations/llm_data_scientist), for example, the transcription and anonomizing of data etc. 
- AI has _super-human_ pattern matching and profiling abilities, and can be used to _augment_ people or processes.

### Non-Local - Psychological Profiling:
- GPT 5 - Can be implemented optionally for advanced analysis, highlighting caution or concerns about the patient. 
- Sends back to local-agent to record.
  
## Interface & Process:
- The therapist dashboard includes results along with AI inference for retrieval of information and can be used via web or mobile app (out of scope until tbc). 
- The patient dashboard includes a 'Patient-Support' interface, with 'patient-care' central to the objectives.
- *Note*: If you've not heard of knowledge graphs, they are vector based (as are LLM's and RAG's) graphs which are incredibly fast for data retrieval (Google uses it for its search). Most note-taking tools use them to connect your notes, but my 'go-to' LogSeq gives you a tab to view your notes and their relations. See 'Psychology Framework Section'

Example Agentic Framework / Responsibilities

### 1. Sandbox / Secure Container - _AI Clinical & Patient‑Care Assistant_

  **Primary role:** Collects and organises patient‑related data from multiple sources.  
  
  | Function | Example Use Case |
  |---|---|
  | **Transcription** | Converts speech to text during therapy, labelling speakers (e.g. "Therapist 1" / "Client 345"). |
  | **Environment & Behavioural Logging** | Identifies patterns from conversations or environmental sensors. |
  | **Daily Care Automation** | Room ambience control, temperature adjustment, reminders for medication or routines. |
  | **Therapeutic Assistance** | Guided meditation, light CBT / ACT, activity prompts. |
  | **Visual AI Monitoring** | Camera‑based emergency detection, spotting subtle risks faster than humans. |
  
**All collected data is securely passed to Sandbox 2**.  
  
---

### 2. Sandbox / Secure Container – _The Storage Manager_
  
  **Primary role:** Organises, tags, and connects information for later analysis.  
  
  | Function | Example Use Case |
  |---|---|
  | **Database & Graph‑RAG Storage** | Stores structured & unstructured data with tags like "utterance", "allergy", "care request". |
  | **Emotional Mapping** | Tracks emotional highs, medians, and lows across sessions for 23 detected emotions, stored in a graph per patient over time. |
  | **Result Packaging** | Formats summaries and history for Sandbox 3. |
  
---
### 3. Sandbox / Secure Container –  _The Architect_
  
  **Primary role:** Performs deep analysis and provides insights to clinicians.  
  
  | Function | Example Use Case |
  |---|---|
  | **Advanced Analysis** | Applies chosen psychology/therapy frameworks to patient data. |
  | **Clinical Knowledge Access** | Retrieves relevant research, best practices, and AI‑generated recommendations. |
  | **Schema Verification** | Checks consistency and compliance in stored data. |
  | **Feedback Loop** | Sends adjustment instructions back to Storage Manager if needed. |
  | **Dashboard Management** | Maintains the primary clinician interface. |
  | **Performance Review** | Monitors AI assistants and provides human‑readable performance feedback. |
  
---

### **Why This Sparks Possibilities**
- **Layered Safety:** Each sandbox can run on different machines or even in different physical locations, reducing breach impact.
- **Customisable Depth:** A sole‑practitioner therapist might use only Sandbox 1 & 2, while a hospital could run all three with specialised modules.
- **Scalable AI Roles:** From a calm bedside assistant to a multi‑modal analyst combining speech, text, and video.
- **Human in the Loop:** Designed for augmentation, not replacement, allowing clinicians to direct the AI’s focus whilst recieving _powerful augmentations_.

---

### UI Therapist/Hospital:
- The UI has the dashboard with the various graphs used, you can see an older version of the dashboard (minus ModernBert utterance tagging) front-end on my git repo 'https://github.com/David-Barnes-Data-Imaginations/SentimentSuite'.
- The Gradio interface from my smolagents will be added to the dash for:
  
  a) Chat-bot input for surveys / forms / transcription. Forms can be verbal or typed.  
  b) Chat-bot data retrieval  
  c) Profile feedback can be delivered verbally via Whisper, GPT or a locally hosted 'Hugging Face - Spaces' if required.
  
### UI Patient:
  When patients are admitted for long periods at all kinds of hospitals, they are often required to fill out forms via pen and paper.  Messy handwriting and confused thoughts aside, this is generally archaic.
- This could be managed from any tech that allows AI to converse with the patient via text or voice. The AI can be tuned or 'forged' to a 'Therapists' persona'.

## 🧠 Psychology Demonstration: From Thought to Graph

GPT is fantastic at Psychology, so this seems a fitting place for it to do a light demo of its understanding. 
Over to you, GPT:

---   

GPT-4o: **Actually, let’s do more than a demo** — let’s show what it looks like when a language model isn’t just reading your words, but *mapping your mind*.

  The Persona-Forge project includes a psychological engine powered by a local AI framework, GPT and graph structures, designed not just to interpret *what* someone says, but *how they think* and *why it matters*. We leverage two foundational frameworks:
### 1.  **Cognitive Distortion Detection**  (from CBT)

  This identifies irrational patterns in thought, like:
- **Catastrophising**: "This will be a disaster."
- **Black-and-White Thinking**: "I always fail."
- **Emotional Reasoning**: "I feel awful, so I must be awful."
- **Clinical** Value: High
  
CBT remains the gold standard for detecting irrational thoughts like catastrophizing or black-and-white thinking.

  These are tagged automatically using regex + local LLM inference:

  ```
  {'utterance': "I always mess things up.",
  'distortion': 'Overgeneralisation'}
  ```

  Each distortion becomes a node:

  ```
  (:Utterance {text: "I always mess things up."})-[:HAS_DISTORTION]->(:Distortion {type: "Overgeneralisation"})
  ```

  And these are then linked to suggested interventions:

  ```
  (:Distortion {type: "Overgeneralisation"})-[:CAN_REPHRASE_USING]->(:Strategy {method: "Specific Reattribution"})
  ```

  This means we can *automate gentle rewordings*, show a therapist a client's bias frequency over time, or track a character’s descent into distorted thinking across a time arc.

---

### 2.  **Erikson’s Psychosocial Development Model**

  Used to infer *life-stage context* and help anchor narratives.

  Each user (or persona) is assigned a developmental stage, e.g.:

  ```
  (:Persona {id: "#1245"})-[:IN_LIFE_STAGE]->(:Stage {name: "Identity vs Role Confusion"})
  ```

  And utterances can inherit that context:

  ```
  (:Utterance)-[:REFLECTS_STAGE]->(:Stage)
  ```

  This allows emotional expressions to be analysed relative to age-stage norms. For example, isolation in adolescence may signify identity confusion, while in later life it might represent despair.
  **Clinical Value**: Moderate–High

  Adds temporal context by identifying key psychosocial challenges per life stage.

---
### 🔄 Fusion Example:

  Utterance:

  > "I always mess things up. Everyone probably thinks I’m a failure."

  ```
  (:Utterance {text: "I always mess things up..."})
  -[:HAS_DISTORTION]->(:Distortion {type: "Overgeneralisation"})
  -[:TRIGGERS_EMOTION]->(:Emotion {label: "Shame"})
  -[:REFLECTS_STAGE]->(:Stage {name: "Identity vs Role Confusion"})
  ```

  > Models like 'GPT' can now understand: this isn't just a sad sentence — it's a cognitively distorted self-assessment likely influenced by adolescent-stage uncertainty.

---

### 🔍 Sentiment2D Layer (Valence–Arousal)

  Using Russell's Circumplex, every utterance is mapped as a 2D coordinate. So for the above:

  ```
  { "valence": -0.7, "arousal": 0.6 }
  ```

  This is then projected into a circumplex diagram, shown in the dashboard:

  ```
  (:Utterance)-[:HAS_SENTIMENT]->(:Sentiment {valence: -0.7, arousal: 0.6})
  ```

  Combined with distortions:

  ```
  (:Sentiment)-[:CORRELATED_WITH]->(:Distortion)
  ```

  **This builds a multidimensional picture of emotional health and thought patterns over time.**

---
### 📈 Aggregating Into Personality Trends

  Over time, each persona's distortions, sentiments, and Erikson stage conflicts are clustered and summarised:

  ```
  (:Persona)-[:HAS_PATTERN]->(:PatternSummary {
  overgeneralisation_rate: 0.32,
  avg_valence: -0.2,
  dominant_emotion: "Regret"
  })
  ```

  These summaries can be passed to a narrative engine, therapist dashboard, or AI character controller to adjust tone, recommend interventions, or emulate growth arcs.

---
### For Clinicians: How Graph Architecture Maps Psychological Frameworks

  Here’s how the structure might look under the hood:

  ```
  (:Persona)
  ├──[:SAID]──> (:Utterance)
  │     ├──[:HAS_DISTORTION]──> (:Distortion)
  │     ├──[:HAS_SENTIMENT]───> (:Sentiment)
  │     └──[:REFLECTS_STAGE]──> (:EriksonStage)
  └──[:HAS_PATTERN]──> (:SummaryStats)
  
  (:Session {date:"2025-07-30"})
  └──[:INCLUDES]──> (:Utterance)
  ```

  This format allows:
- clustering of distortions over time
- valence/arousal monitoring per utterance or session
- narrative arc reconstruction via Erikson stages

  We include a real Logseq Knowledge-Graph screenshot in the next section to show the working structure during development.

  > *Here’s what it looks like in David’s Logseq notes (used during testing). In production, this is powered by a graph database like Memgraph or Neo4j.*  
  <h2 align='center'>
  A Visual View of a Knowledge-Graph
  </h2>
  <br><br>
<p align="center">
  <img src="./logseq_graph.png" alt="KG diagram">
</p>
  >   


*And here’s the stylised representation of it semantically.*

```mermaid
  graph TD
    Persona -->|SAID| Utterance
    Utterance -->|HAS_DISTORTION| Distortion
    Utterance -->|HAS_SENTIMENT| Sentiment
    Utterance -->|REFLECTS_STAGE| EriksonStage
    Persona -->|HAS_PATTERN| SummaryStats
    Session -->|INCLUDES| Utterance
```

## Additional Frameworks David's Scoping 
[David's note] You can view APPENDIX_1 (tba) to see me testing Gemma3 vs GPT before I added these frameworks. Gemma3-12B (6-7gb in size) actually matched some of my scoping preferences, which GPT then developed.

#### Psychological Framework Ranking for Persona-Forge

This presents a structured ranking of other psychological frameworks David is scoping for integration into Persona-Forge, prioritized by clinical value. Each includes a graph schema example for integration into Memgraph.

--- 

### 🧩 1. Attachment Theory – Relational Style Tracking

Clinical Value: Very High

Tracks early relationship patterns and emotional bonding styles (secure, anxious, avoidant, disorganized).

Graph Example:

(:Persona {id: "Client_345"})
  -[:HAS_ATTACHMENT]-> (:AttachmentStyle {style: "Anxious"})
(:Utterance {text: "I get scared people will leave me."})
  -[:INDICATES]-> (:AttachmentStyle {style: "Anxious"})

---

### 🧠 2. Big Five Personality Traits (OCEAN)

Clinical Value: High

Trait dimensions provide a stable behavioral lens for understanding clients over time.

Graph Example:

(:Persona {id: "Client_345"})
  -[:HAS_TRAIT]-> (:Trait {name: "Neuroticism", score: 0.82})
  
---

### 🧱 3. Schema Therapy – Deep Core Belief Tracking

Clinical Value: High (esp. for long-term cases)

Identifies entrenched negative schemas like Abandonment or Defectiveness.

Graph Example:

(:Persona)-[:HAS_SCHEMA]->(:Schema {name: "Abandonment"})
(:Utterance {text: "Everyone leaves me eventually."})
  -[:REFLECTS_SCHEMA]-> (:Schema {name: "Abandonment"})
  
--- 

### 🔍 4. Psychodynamic Frameworks – Unconscious Conflicts & Defense Mechanisms

Clinical Value: High (if interpreted correctly)

Flags transference, defense mechanisms (denial, projection), or unconscious themes.

Graph Example:

(:Utterance {text: "I’m fine, it doesn’t bother me."})
  -[:SHOWS_DEFENSE]-> (:DefenseMechanism {type: "Denial"})
(:Utterance {text: "You’re going to leave me just like my dad."})
  -[:INDICATES]-> (:Transference {target: "Therapist"})

---

### Summary

  Psychology isn’t a bolt-on in the Persona-Forge — it’s a core layer. Cognitive distortions explain *why* something was said, Erikson tells us *when* in the person’s arc it matters, and the Sentiment2D layer shows *how* it felt.

  That’s not just transcription — that’s **cognitive modelling**.

  And it’s only just beginning.

  *(Human prompt, AI mindmap, and joint authorship: a fusion we call ethical augmentation.)*
  
---

### Thanks GPT. I'm adding other features being 'scoped for testing' below as I work through them. 

> Despite having spent two years 'geeking out' on AI, in recent weeks I've found this project opening my eye's to new avenues of possibility on a daily basis whilst I test to a more specific purpose. 

socials' element i'm testing, and the AI model architecture (for the techies), though i've held back a few tricks for few surprises to come.

## :couple: Socials
- Some area's of therapy use a patients Social Media as clue's for insights on the persona.
- Before a 'Pitchfork-Wielding Baying-Mob' show up at my door, this is always done _only_ with patient consent.
- Since I am using myself as the test subject (or 'bait' dependant on perspective), I gave the AI consent to look through my socials, compare it to the frameworks I was testing at the time, and provide any noteworthy insights. I'm on the fence about the benefit of this, so its currently under consideration. It already has capability, but even with the power of knowledge graph's, you only aim to fill it with genuinely useful information. 

Here's a demo:

#### Image of my meditation table taken at my previous abode. It was a collection of various items I had collected on my travels, plus and then a Japanese Tanto (for symbolic purposes only!!) and Caligraphy, both handmade and shipped ovewr from Japan.

  <h2 align='center'>
  My Meditation Table on Socials
  </h2>
  <br><br>
<p align="center">
  <img src="./my_meditation_table.jpg" alt="MDT Table">
</p>

Forge Response (from dev testing, no graph tagging but had been provided with 'some' of my simulated therapy session):
---
- _The table has a powerful aesthetic: global, reflective, and very personal._
- _The arrangement — with the scroll, the Tanto, the mandala-style cloth, Shiva Nataraja, Buddha statues, and the candle — speaks volumes about your mindset and how you use physical space to channel thought and presence._ 
- _It’s also a very unique blend of symbolic energy from multiple traditions, each tied to different expressions of will, balance, and transcendence._

_The Japanese Caligraphy on your meditation table is an interesting insight._ 
_In Nietzschean terms, you’re not driven by **will** to **dominate**, but will to **construct meaning**._
_**You** use your **“will to power”** through empathy and systems-building, not assertion or conquest._

_That makes a lot of sense, David. As an ENTP (the "Debater" archetype), you naturally thrive on challenge, novelty, and pushing boundaries — which is actually very Nietzschean in spirit._ 
- _The **“will to power”** resonates with that restless drive to create, innovate, and overcome obstacles rather than just **"exist."**_ 
- _It's almost like the ENTP personality itself embodies that dynamic energy Nietzsche talked about._

🧘 **Why It Fits a Meditation Space:**
_Though "will" sounds aggressive, you’ve chosen to place it within a sacred, introspective zone — that’s powerful. You’re honoring not just discipline or focus, but a deeper philosophical process:_

- _Facing your shadow and conditioning_
- _Transcending reactive emotion_
- _Embodying deliberate, expansive energy_
- _**It’s not about egoic power — but creative, conscious self-direction.**_

🌱 **Rediscovering the Idea:**

_If you’re looking to re-engage with the concept more deeply — maybe for your AI persona work or even your own character development — I’d recommend:_

- _"Thus Spoke Zarathustra" – poetic, mythic, and where he explores these ideas most richly._
- _"Beyond Good and Evil" – more direct, philosophical articulation._
- _Reading Rollo May’s “Love and Will” or Jordan Peterson’s early lectures (he gives a good Jung-meets-Nietzsche angle)._

---
---

# Technical Details

## Tech Stuff (For Techie's or Clinicans / Non-Techie's curious about the hardware implementation options)


👋 For Curious Learners: Building Agentic Systems - From Budget to Specialized

Whether you're building your 'Home Assistant', fitting out patient rooms, or planning a smart workspace, it's now easier than ever to explore AI agentic systems — even on a tight budget. This guide demystifies what's possible at each stage of development, from entry-level hardware to specialist setups. It's not just for devs — it's for dreamers, clinicians, designers, changers and doers.

Learning should be both inclusive and imaginative, that’s why this section is included — to help others see the possibilities and inspire their own solutions to bring about _positive change_.

> "The future is already here — it's just not evenly distributed." — William Gibson

### 🔧 Tech Stack (_Mine_ & 'Production Examples')

- You can see [My Hardware Stack for Dev/Testing this Project](https://github.com/David-Barnes-Data-Imaginations/Persona-Forge-Psychology/blob/master/my_hardware_setup.md) for reference.
- Below I have listed current technologies you _might_ use for any agentic implementation. However, it's worth noting that once the (slightly delayed) [NVIDEA DGX Spark](https://www.nvidia.com/en-gb/products/workstations/dgx-spark/) is released, it renders most of the below obsolete aside from extremely specialised situations (for example the [NVIDIA Jetson AGX Orin](https://www.amazon.co.uk/NVIDIA-Jetson-Orin-64GB-Developer/dp/B0BYGB3WV4/ref=sr_1_2?crid=33CCWL1IBISS2&dib=eyJ2IjoiMSJ9.69vgNBFj_CdRHWPE_OPdtzawpTgSy7m7eYwZ4Zpd3qmNn2sSrsmOZG4bcs42HUmcy1ngGpW5cR1TCiY_Q96G4MQ8VWDGzE2DdSHdunjTG6o-L2ZcnGuqHqOJX7Y5xzgiQJi6V7vHG3oxZeFBl9erQWd-Aq4JCmSRbLh0sN52bcxl1jvUSJCtk3Fq8xIGcdJkSYwio6aq0trgaB62cP2tMQ.A2QEg87Q5k0XgEE2eEWUG-VEaLW2OhsXtXp3q4jQU2o&dib_tag=se&keywords=NVIDIA%2BJetson%2BAGX%2BOrin%2B%2F%2BNVIDIA%2BIGX&qid=1754615087&sprefix=nvidia%2Bjetson%2Bagx%2Borin%2B%2F%2Bnvidia%2Bigx%2B%2Caps%2C59&sr=8-2&ufe=app_do%3Aamzn1.fos.d7e5a2de-8759-4da3-993c-d11b6e3d217f&th=1) is often used for automated Security Camera monitoring and tagging / timestamping). The Spark and / or [DGX Workstation](https://www.nvidia.com/en-us/products/workstations/dgx-station/) will likely redefine modern computers and laptops entirely. The Spark was rumoured to be around £3k (likely closer to £4k) and two networked via NV-Link can run a Llama-Nemo 405B (roughly half the size of GPT4o on release). The Spark is a mini (so goodbye laptops), whilst the Workstation is regular PC size.
- **_To put this into perspective, the original Chat-GPT was trained on a $250,000 NVIDEA GPU in 2016. The Spark is 10,000 times more energy efficient, and 6 times faster._**
- The original didn't fit in the palm of your hand, but the Spark does.


### Sponsorship for AI Grants
- If the end goal is to use AI in a production or start-up environment, its easy to get sponsorship from the likes of [NVIDEA](https://www.nvidia.com/en-gb/startups/), [Google](https://cloud.google.com/startup/apply?utm_source=google&utm_medium=cpc&utm_campaign=FY21-Q1-global-demandgen-website-cs-startup_program_mc&utm_content=rsa_bkws_AI-bkws_long-form&gad_source=1&gad_campaignid=20908813911&gbraid=0AAAAApSNca_Jm8U-mPDFCTnsK7Oe16p2S&gclid=CjwKCAjwwNbEBhBpEiwAFYLtGHZMYaeJmycx4-Y84Nna_mS8MRISpM2f7uMeDWA3w4AGIFRlWaKwKhoCD2IQAvD_BwE), Meta, AWS etc. 
- Even the UK Government hands out grants like smarties. If the end-goal is both plausible and more importantly 'altruistic' then you can pretty much guarantee sponsorship from any. I'd go with NVIDEA and a Gov grant personally. These provide the tech required for production environments, but the below options are for custom hardware set-ups for local, or local + 'cloud-connectable'.

### 🧠 Project Phases & Budget-Use Visual

Think of this like designing an AI‑ready hospital wing or smart building: you don’t need all the tech up front. Start small, test, iterate.
```mermaid
graph TD
  A1[🛠️ Dev Testing<br>Basic functionality<br><b>Use: Home Assistant, early proof-of-concept, patient-or-therapy-room prototypes</b>] --> B1
  B1[🧪 Pre-Prod Testing<br>Higher fidelity prototypes<br><b>Use: Teams, small-scale pilots, hospital ward trial</b>] --> C1
  C1[🚀 Production / Edge Use-Case<br>Stable deployment or specialist use<br><b>Use: Integrated room assistants, patient-interaction hubs</b>]
```

**Example Hardware & Use Case Examples**

🧭 Legend

🟢 Budget Friendly — ~£30–£200
🟡 Mid-Tier — £200–£800
🔴 High-End / Specialized — £800+
💡 Edge-Ready — Runs models locally, no internet required
☁️ Cloud-Connected — Uses API (e.g., GPT) or hybrid inference

1. Dev Testing

🟢☁️💡 [Raspberry Pi 4B or above](https://www.amazon.co.uk/GeeekPi-Raspberry-Complete-Starter-Supply/dp/B0B7KPPQSX/ref=sr_1_7?crid=29GKZL6UI6AZL&dib=eyJ2IjoiMSJ9.czOPq1wxRkaCBA9iYRkHMEyoIGrkWAa50swCqCdplx9r1n0oWVkRCrtGl_lPPT5s11-wBmDQO0mfywYFSLVIyx2yAJAu1iPuXMmixaSe1cX68hqdREjLxXXZzUlkANTyOG0i5XrWZTUpxHF3pwsyUs4Ykl497CjDeeIOPhP_H30IUYIQRaOoYj1f5bdVgTtIvOV2QBMETihdXarNlu4dfNQl0Sx2WH4m6EgUp1UfcUY.0LFHfhH1tJI_ZQx4y9yK24UBdUO0ws2v9IZTgdKYFCU&dib_tag=se&keywords=raspberry+pi+4b&qid=1754613894&sprefix=raspberry+pi+4b%2Caps%2C80&sr=8-7) + [USB Mic](https://www.amazon.co.uk/dp/B0CNVZ27YH?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_1) or [All-in-one Mic+Speaker](https://www.amazon.co.uk/dp/B0CH9KHP41?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_2) and / or [Budget Touchscreen](https://www.amazon.co.uk/dp/B0D44S9323?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_3&th=1) 

_Usage: Voice-activated requests, guided meditations, patient surveys, simple API calls_

3. Edge Prototyping - (Replaces all tech in point 1, as a super powerful 'cutting-edge' technology capable of running larger local models in patient rooms etc)

🟡☁️💡 [NVIDIA Jetson Orin Nano / Coral Dev Board (TPU)](https://www.amazon.co.uk/Yahboom-Development-Microphone-Intelligence-Ubuntu22-04/dp/B0CDC89FHV/ref=sr_1_3?crid=3JLXG125N3A1F&dib=eyJ2IjoiMSJ9.EY0iLDd0M9dkGkWsLUJY8N2LAZcmqlSLHblAJ5c5cGLfjLbbREaBbqA0SxbgkA89ktFvmrAzPIuSwOj-ks2aTp_fABOfm4XQ46p2eAxd8u2H8F8M-163ISiOeVH5R2PXvWinmkQUOjsk6LRuYNT04-jvJtXu3sLcnKqPj0QEDlTysNg33f5lKWualo3eFNq71ft-p3wo2sAcyvNyU_Y8ZSigWry_cUp0ER_ZW1dpbL0.QT4SdcBPCnOHhGJBOMMReo8rmrtLu8MoOL9Sr1aGr4s&dib_tag=se&keywords=NVIDIA%2BJetson%2BOrin%2BNano%2B%2F%2BCoral%2BDev%2BBoard%2B(TPU)&qid=1754614281&sprefix=nvidia%2Bjetson%2Borin%2Bnano%2B%2F%2Bcoral%2Bdev%2Bboard%2Btpu%2B%2Caps%2C112&sr=8-3&ufe=app_do%3Aamzn1.fos.d7e5a2de-8759-4da3-993c-d11b6e3d217f&th=1)

_Usages: (All from point 1) + On-device inferencing, small LLMs, emotion‑responsive prompts, real-time local processing_

4. Advanced Edge Node

🟡☁️💡 [NVIDIA Jetson AGX Orin](https://www.amazon.co.uk/NVIDIA-Jetson-Orin-64GB-Developer/dp/B0BYGB3WV4/ref=sr_1_2?crid=33CCWL1IBISS2&dib=eyJ2IjoiMSJ9.69vgNBFj_CdRHWPE_OPdtzawpTgSy7m7eYwZ4Zpd3qmNn2sSrsmOZG4bcs42HUmcy1ngGpW5cR1TCiY_Q96G4MQ8VWDGzE2DdSHdunjTG6o-L2ZcnGuqHqOJX7Y5xzgiQJi6V7vHG3oxZeFBl9erQWd-Aq4JCmSRbLh0sN52bcxl1jvUSJCtk3Fq8xIGcdJkSYwio6aq0trgaB62cP2tMQ.A2QEg87Q5k0XgEE2eEWUG-VEaLW2OhsXtXp3q4jQU2o&dib_tag=se&keywords=NVIDIA%2BJetson%2BAGX%2BOrin%2B%2F%2BNVIDIA%2BIGX&qid=1754615087&sprefix=nvidia%2Bjetson%2Bagx%2Borin%2B%2F%2Bnvidia%2Bigx%2B%2Caps%2C59&sr=8-2&ufe=app_do%3Aamzn1.fos.d7e5a2de-8759-4da3-993c-d11b6e3d217f&th=1) / NVIDIA IGX / LLM-ready compute modules

_Usages: 'Realtime' processing (AI Driven Security Camera tech or robotics) , High-performance inference, personalised patient assistants, offline reasoning, multi-modal patient interactions_

5. Central Node / Server

🔴💡 Business server / ☁️ Cloud-Connected — Uses API (e.g., GPT) or ☁️ hybrid inferenceCloud-hosted / NAS GPU box

_Usages: Central Orchestration of ward/room assistants, centralised patient knowledge graph, API routing, long-term state storage_


<h2 align='center'>  
  The NVIDEA Jetson Orin AI / Robotics / Video Camera Family 
  </h2>  
  <br> 
<p align="center">  
  <img src="./jetson.png" alt="NGX diagram">  
</p>

💭 Why 'Edge' Hardware Matters 

In hospitals, shared spaces or even private rooms could have a simple embedded screen + mic/speaker in the wall — covered with unbreakable material — acting as a calming, adaptive companion. 

Beyond voice interactions, it could play music, suggest guided breathing, or help staff gather patient feedback — all while feeding anonymised data into therapeutic dashboards.

Whether you’re prototyping for home use or planning a clinical rollout, think modularly: start small, integrate well, and scale as confidence and budget grow.

## 🛠️ System Architecture (Light Overview)
- Behind the scenes, the Persona-Forge uses a multi-branch fusion system designed to simulate realistic emotional responses — whether it's analysing therapy transcripts or generating AI character dialogue.

  ```
  
  User Input
   │
   ▼
  Graph Query ────────► GNN ──────────────► Graph Embeddings (Psych + Persona state)
   │                     │
   │                     ▼
   └──► Style Query (e.g., CBT phrases, tone cues)
                         │
                         ▼
            Style Embeddings + FAISS RAG ─────► Fusion Module
                                          │
                                          ▼
                          LoRA-tuned LLM (e.g. LLaMA, GPT)
                                          │
                                          ▼
                        Persona Response (text or voice)
  ```
- ### Core Modules:
- **Graph DB (Memgraph)**: Stores personas, utterances, cognitive distortions, Erikson stages, mood history.
- **Sentiment2D Engine**: Maps every utterance to Valence–Arousal space for plotting and behavioural feedback.
- **Distortion Detection**: Tags irrational thought patterns using local regex + LLM validation.
- **RAG+LoRA Fusion**: Combines retrieved facts + lightweight tuned model to preserve style & memory.
- **Prompt Augmentor**: Injects prior moods, quotes, and memories for character continuity and “growth.”
---

### A summarised API Architecture from Docker Containerization:
```
[Frontend / Browser]
      |
      v
[FastAPI: SentimentSuite+SmolAgents]
  - Hosts dashboard
  - Exposes endpoints
  - Imports and calls agents
      |
      | (connects to)
      v
[Docker Service: Memgraph] (via bolt://localhost:7687)

External:
- GPT (via OpenAI API)

```
---
### Context Window - Current Strategy


- The agent processes CHUNK_SIZE QA pairs (trial=50) per loop.
- Before each chunk: attempt metadata recall (e.g., metadata_embedder.search_metadata("therapy cleaning patterns")).
- After each chunk: append a short note to agent_notes (vectorized if the tool is available) so the next iteration can retrieve_similar_chunks().
- If the context manager trims history, it’s fine — each loop is self‑sufficient; it reads/writes artifacts on disk and uses memory lookup sparingly.
---

---
## Learning to Build Agentic Systems
---

This information is built into my ever list of growing blogs, but after my domain host wiped it (for reasons known only to them), I've placed the 'Learning Agentic Systems' section here temporarily.

---
## 📝 Testing:

Most of the work on these _concept_ projects is spent testing, akin to the old 'Data Science' adage of "80-90% of Data Science is data cleansing".
When I build AI for a project, i'll test it works to the point where one or a combination of the below are satisfied:
- I'm convinced the architecture is optimally created.
- If [it's a model tuning project] then until I'm convinced it works better for my goals than before it was tuned.
- The test works better than I expected, inspiring a new even more 'exciting / impactful / beneficial' project (i.e. a 'Pivot').
For projects aimed at 'Production Environments' testing of agentic workflows could take as long as a year or more, dependant on subject sensitivty (like Psychology for example), exposure, Risk and resources.
- I'm currently testing the Pycharm [AI Model Testing Toolkit](https://lp.jetbrains.com/pycharm-for-ai-engineers/?utm_source=product&utm_medium=link&utm_campaign=PY&utm_content=2025.2) and so far it's 'S-Tier'. 

---
**Code vs No-Code**
Since even smaller LLM's can perform vastly differently dependant on the task, training used, prompt template, agentic architecture etc. Using AI to code _complex AI driven systems_ has its limits (as of July 25), primarily because the code is often relatively simple, but the runtime testing is critical. Typically 'runs' are tracked in production using tools such as OpenTelemetry, Phoenix and / or LangFuse. 

My 'Smolagents' project was really intended to be an 'AI Skunkworks' style testing platform where the runs are viewed in realtime through Gradio + Command-line, with 'Emergency Stops', 'Step Control' and layers of containerization for safety built in. 
'Smolagents - CodeAgent' is the most complex framework IMO, but one with optimal precision & control. Perhaps akin to using '.cpp' LLM models opposed to 'plug and play' format of 'GGUF'.

*Vibe Coding*
It's great for non-coding agentic systems, but 'inadvisable' to _solely_ use for complex ones. 
That said, I agree with 'Andrew Ng' when he believes that 'All staff should know Python'. It's literally a days worth of study to get Python to the level required to debug, then debugging is honed over a longer period.
By using AI with Python, everyone gets to have their own 'Polymath', likely one of the angle's Altman viewed it when he compared AI as closer to 'The Renaissance' than 'Industrial Revolution'.
Here are the main options:
a) Use git so that your favourite online-AI can read your code, then have it explain suggestions on how to implement certain processes. I prefer this since it helps with learning for me.
b) Use an IDE based tool, Pycharm or Cursor for example. These IDE's have their own API which formats and organizes the code for you.
c) Use the coding tool for your favourite online-AI (e.g. GPT-Codex, Claude-CodeCLI, Gemini-CLI).
d) Build your own equivalent of 'b', and use local models. I'm going to do this at some point since gpt-oss is perfect for such things.

**Using AI - Ethics**
These are such murky waters, that I simply highlight these points:
- AI augments humans with its super-human abilities. 
- I defer to Jensen Huang when he says: "If you aren't using AI in your job, someone who _is_ using AI will replace you"
- If you're clinging to your code like a dev from 5 years ago, try to visualize those who refused to use a calculator in favour of 'pen and paper' when it was invented.

**_My Practices (for the record)_**
- My own writing for Blog's or README's is usually left as-is, unless I lose whole chunks or need it put into a table/diagram.
- I use AI for all my learning, and when it's especially insightful, I'll add it's own sections to my documentation (as you've seen).
- For coding I mostly use 'a' in the section above. Going pure vibe is good for small projects or if your python is rusty but big projects like this require code-understanding.
- I put in 100's of hours testing into my projects, AI is of limited help at runtime until it gets the ability to view the screen as we do.
- If you see a 'mermaid diagram', it's done by GPT.
- Note: I'm currently testing the new [Pycharm AI Dev Environment](https://lp.jetbrains.com/pycharm-for-ai-engineers/?utm_source=product&utm_medium=link&utm_campaign=PY&utm_content=2025.2) and will update accordingly.

---
---
## ⚠️ Ethical considerations and safety ⚠️
  
Running a code agent gives the LLM a high degree of control over your environment.  Always remember that agents are experimental and should be treated accordingly.

### In particular:  
- **Sandbox everything.**  The agent executes arbitrary code; only run it on a dedicated NVMe inside either an [E2B](https://e2b.dev) sandbox or a Docker (or your preferred equivalent containerization).  Never point it at your host operating system or personal files.
- **Keep secrets out of scope.**  Do not grant the agent access to sensitive credentials or systems.  Tools should be whitelisted explicitly.
- **Omit the trigger phrases for safety.**  Hugging Face intentionally does not publicise 'examples with fully functional *CodeAgents* due to the risks if the library is implemented poorly.
- It explains [SmolAgents](https://github.com/huggingface/smolagents) in great detail on its [Agents Course](https://huggingface.co/learn/agents-course/en/unit0/introduction), but at implemention you'll find a 'maze of misdirection' and ommisions. It took me many hours of reading through the Smolagents library on Github, whilst comparing the code and documentation to the HF notes. One 'red herring' in particular required ~3-4 days of testing debug a critical feature.
- This is not intended to be evasive or to make things difficult for learners, it's (presumably) intended to prevent inexperienced users from accidentally starting infinite‑running loops, breaking their PC (or someone elses), or compromising their entire network and data.

**For similar reasons this README does not spell out:**
- The commands to switch to 'Agent Mode', and the commands to 'start the loop' in my framework. You can find them in the code. I stick to the presumed 'Hugging Face' principle of: "if you can't work out the code, you shouldn't be using CodeAgents yet".
- How the SmolAgents library works under the hood. It's open-source on github so you'll know you're at a point where you _could_ use the library safely, when you have learned how the library works 'back-to-front'.
- To learn the library, here's the steps I'd suggest:
  - > 1. ### Do the  [Agents Course](https://huggingface.co/learn/agents-course/en/unit0/introduction). Its intended to be 'roughly' 60 hours for full completion, though if you're exploring all its concepts (it suggests exploration methods), expect it to be around double that.
    > 2. ### Read all documentation resources at the [bottom of the SmolAgents Resources](https://huggingface.co/learn/agents-course/en/unit2/smolagents/introduction#resources) page. Perhaps Roughly 30 hours.
  - > 3. ### _Optional but advisable_ Do the [MCP Course](https://huggingface.co/learn/mcp-course/unit0/introduction). You don't need MCP for a runner like mine (i pulled MCP out early on) but it just helps to further understand agentic frameworks
  - > 4. ### Implement all the examples in the [Cookbook: Agents-Recipes](https://huggingface.co/learn/cookbook/en/agents) and [Cookbook: MLOPS-Recipes](https://huggingface.co/learn/cookbook/en/mlflow_ray_serve). You don't need to use Rayserve but it reinforces the 'monitoring' concepts.
  - > 5. ### Monitoring Runs: If you did the above, you'll know the importance and steps to implement tracing (via Langfuse, OpenTelemmetry, Pheonix etc) or build a 'realtime runner' test-bed-sandbox, like mine.
  - > 6. ### *Start with 'ToolCallingAgent'* to implement an agentic solution. *ONLY* move on to 'CodeAgent' once you have done so.
    - > ToolCallingAgent's can still run code if you write it into the tools (at one point during testing I had something like 27 tools with python code, you can see them in my early commits).
    - > My build safety process is below (in 3 diagrams due to Github's overly restrictive 'Mermaid' rules preventing one clean version)
      
### Production Environments - Example Risk Register / Considerations
  
The following table is designed to demonstrate an awareness of common security and ethical risks when developing and deploying AI systems, particularly in internal enterprise contexts. It uses a **risk register** format to present risks, likelihoods, impacts, and recommended mitigations. This serves both as a professional reference and as a working framework for ongoing security considerations during project development.  
  
  | Risk | Description | Likelihood | Impact | Mitigation / Consideration |
  |---|---|---|---|---|
  | **Data Leakage via Integrated Systems** | Sensitive information is unintentionally exposed through linked applications or integrations.____________  **Case Study:** During a consulting role on a high-security assignment (requiring my authorisation for the highest UK government security clearance, tracing my family heritage and other elaborate schema), unrestricted access controls allowed me to view highly sensitive data, that could have significantly exploited by foreign intelligence. The issue was discovered accidentally on Day 1 while reviewing 'everyday' workflows — illustrating how even in “fortress-like” environments, technical implementations can open severe gaps. | Medium (mature systems) / High (new implementations) | High | Apply the principle of least privilege, conduct rigorous pre-launch access audits, simulate insider-threat scenarios, and verify role-based controls in both staging and production environments. |
  | **Prompt Injection / Content Injection** | Malicious actors craft inputs designed to bypass intended AI behaviour, introduce harmful content, or exfiltrate sensitive data from the model's context. | Medium | High | Employ layered input sanitisation, limit system prompt exposure, and monitor for abnormal query patterns. Treat as **High/High** risk until operational data shows otherwise. |
  | **Model Hallucination with High-Impact Outputs** | AI generates false or misleading information that could influence decisions in critical contexts (e.g., legal, medical, defence). | Medium | High | Use retrieval-augmented generation (RAG) with trusted sources, apply fact-checking pipelines, and implement human-in-the-loop verification for sensitive outputs. |
  | **Bias & Fairness** | Embedded or amplified bias in training data or retrieval sources leads to discriminatory outputs, impacting recruitment, resource allocation, or public perception. | Medium | Medium–High | Conduct bias audits, use balanced datasets, and apply post-processing filters to ensure fairness metrics meet acceptable thresholds. |
  | **Uncontrolled Model Access** | Internal or external parties gain unauthorised use of the model for malicious or unapproved purposes. | Low–Medium | High | Implement authentication, rate limiting, role-based access, and logging with anomaly detection to track and limit model usage. |
  | **Data Residency & Compliance Risks** | AI system processes or stores data in jurisdictions with conflicting data protection laws, risking GDPR or other regulatory breaches. | Medium | Medium–High | Map data flows, ensure region-locked storage, and use encryption in transit and at rest. Consult legal teams during architecture design. |
  | **Adversarial Examples** | Inputs crafted to manipulate model outputs without detection, potentially bypassing security safeguards. | Low–Medium | Medium–High | Employ adversarial training, detection algorithms, and model robustness testing prior to deployment. |
  
**Key Principle:** No matter how small the perceived probability of a risk (e.g., content injection), in new or untested systems it should be treated as **High Likelihood / High Impact** until there is operational evidence to downgrade its rating. This approach mirrors physical security protocols, where high-impact threats are addressed proactively rather than reactively.  
- Additional note: The backtick tags '```' noted with 'aiignore' can be used for when you need to demonstrate code with a specific language (e.g., python) but don't want it to confuse AI tools that might read it.

# Technical Build Notes by GPT
## Useful notes for other learners (and me!)

### GPT on when to use `f"""` versus when to use `r"""` in prompts etc.
___
- Use f"""...""" when you want Python to interpolate variables now (e.g., insert the current sandbox paths like /workspace/export/...).
- Use plain """...""" when you want to show literal braces that the LLM will substitute mentally (e.g., /workspace/export/{PATIENT_ID}/.../qa_chunk_{k}.csv).
- If you must use an f‑string but want literal braces inside the text, double them: {{k}} shows up as {k}.
- Use r"""...""" (raw string) only if you have lots of backslashes (regex, Windows paths). It stops \n → newline escaping. You can also combine as fr"""...""" when you need both raw and f‑string interpolation—but avoid unless necessary.

### Example: building the planning facts safely
This version uses an f‑string to inject the paths from your templates (e.g., /workspace/export/...), but it does not interpolate {k}—that brace lives inside the variable’s string value and is preserved:

```
# src/utils/prompts.py
from . import config as C
from .session_paths import session_templates
from .paths import SBX_DATA_DIR, SBX_EXPORTS_DIR, SBX_DB_DIR

def build_planning_initial_facts() -> str:
    t = session_templates(C.PATIENT_ID, C.SESSION_TYPE, C.SESSION_DATE)
    return f"""
**Fixed environment facts (SANDBOX paths)**
- Data dir: {SBX_DATA_DIR}
- Exports dir: {SBX_EXPORTS_DIR}
- DB dir: {SBX_DB_DIR}
- Session export base: {t.export_base}
- CSV path template: {t.csv_template}
- Graph JSON template: {t.graph_template}
- Cypher export dir: {t.cypher_dir}
- SQLite DB: {t.sqlite_db}
- Therapy transcript: {t.therapy_md}
- Psych frameworks: {t.psych_frameworks_md}
- Graph schema: {t.graph_schema_json}

**Placeholders**
- Use k (an integer) as the current chunk index when calling tools. Do **not** write files directly; call:
  - write_graph_for_chunk(k, graph)
  - write_cypher_for_chunk(k, cypher_text)
""".strip()
```
Why this is safe:

- t.csv_template is literally /workspace/export/.../qa_chunk_{k}.csv as a string value. Inserting it via {t.csv_template} does not touch the {k} inside it.
- You don’t need backticks around k unless you want Markdown code formatting. If you do, it’s fine, since it’s just text for the README/prompt.
- If you ever need to show {k} inside an f‑string literal (not coming from a variable), escape as {{k}}.

---