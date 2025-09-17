// ============================================================================
// TEXT CHUNK GRAPH SETUP - Constraints and Indexes
// ============================================================================

// Create constraints
CREATE CONSTRAINT textchunk_id IF NOT EXISTS FOR (t:TextChunk) REQUIRE t.id IS UNIQUE;

// Create indexes for framework nodes
CREATE INDEX emotion_name IF NOT EXISTS FOR (e:Emotion) ON (e.name);
CREATE INDEX distortion_type IF NOT EXISTS FOR (d:Cognitive_Distortion) ON (d.type);
CREATE INDEX attachment_name IF NOT EXISTS FOR (a:Attachment_Style) ON (a.name);
CREATE INDEX defense_name IF NOT EXISTS FOR (m:Defense_Mechanism) ON (m.name);
CREATE INDEX schema_name IF NOT EXISTS FOR (s:Schema) ON (s.name);
CREATE INDEX stage_name IF NOT EXISTS FOR (es:Erikson_Stage) ON (es.name);

// Create vector index for embeddings
CREATE VECTOR INDEX textchunk_embedding_index IF NOT EXISTS
FOR (t:TextChunk) ON (t.embedding)
OPTIONS {indexConfig:{
  `vector.dimensions`: 768,
  `vector.similarity_function`: 'cosine'
}};

// ============================================================================
// TEXT CHUNK NODES AND RELATIONSHIPS
// ============================================================================

// Create TextChunk nodes with properties
UNWIND [
  {"chunk_id": "s001.qa_pair_001.c1", "text": "If I experience emotions directly about myself, they are under-stated to say the least. Rather it feels like I feel emotions through others, reflecting their feelings, or my perception of their feelings, opposed to having feelings about myself.", "source": "therapy.md", "framework_tags": ["Emotion:Empathy", "Attachment:Anxious_preoccupied"], "valence": 0.0, "arousal": 0.0, "confidence": 0.8, "timestamp": "2025-09-17T15:52:46Z", "qa_id": "qa_pair_001", "session_id": "session_001"},
  {"chunk_id": "s001.qa_pair_001.c2", "text": "If I\u2019m with someone who\u2019s happy, I feel happy. If I\u2019m with someone sad, I feel sad. I don\u2019t remember ever sitting around feeling sorry for myself, likewise I don\u2019t sit around feeling joy about myself.", "source": "therapy.md", "framework_tags": ["Emotion:Empathy", "Attachment:Anxious_preoccupied"], "valence": 0.0, "arousal": 0.0, "confidence": 0.8, "timestamp": "2025-09-17T15:52:46Z", "qa_id": "qa_pair_001", "session_id": "session_001"},
  {"chunk_id": "s001.qa_pair_001.c3", "text": "I do often use \u2018creative visualisation\u2019 to simulate emotions if it's going to serve a purpose. For example, in the gym when I\u2019m lifting weights, I will typically visualise something that would make me angry, as it \u2018feels\u2019 like it gives me extra strength. Friends have often said to me they saw me in the gym, but I walked right past them with a vacant look in my eyes, or one person hilariously described it as 'crazy eyes'! There's nothing crazy / angry figuratively however, it's just a side effect of me trying to disconnect so much visual brain-space to make room for the visualization. I literally never remember even seeing them.", "source": "therapy.md", "framework_tags": ["Emotion:Anger", "Defense:Dissociation", "Schema:Emotional_deprivation"], "valence": -0.5, "arousal": 0.7, "confidence": 0.8, "timestamp": "2025-09-17T15:52:46Z", "qa_id": "qa_pair_001", "session_id": "session_001"}

] AS c
MERGE (t:TextChunk {id: c.chunk_id})
SET t.text = c.text,
    t.source = c.source,
    t.framework_tags = c.framework_tags,
    t.valence = c.valence,
    t.arousal = c.arousal,
    t.confidence = c.confidence,
    t.timestamp = datetime(c.timestamp);

// Link chunks to Session and QA_Pair
UNWIND [
  {"chunk_id": "s001.qa_pair_001.c1", "text": "If I experience emotions directly about myself, they are under-stated to say the least. Rather it feels like I feel emotions through others, reflecting their feelings, or my perception of their feelings, opposed to having feelings about myself.", "source": "therapy.md", "framework_tags": ["Emotion:Empathy", "Attachment:Anxious_preoccupied"], "valence": 0.0, "arousal": 0.0, "confidence": 0.8, "timestamp": "2025-09-17T15:52:46Z", "qa_id": "qa_pair_001", "session_id": "session_001"},
  {"chunk_id": "s001.qa_pair_001.c2", "text": "If I\u2019m with someone who\u2019s happy, I feel happy. If I\u2019m with someone sad, I feel sad. I don\u2019t remember ever sitting around feeling sorry for myself, likewise I don\u2019t sit around feeling joy about myself.", "source": "therapy.md", "framework_tags": ["Emotion:Empathy", "Attachment:Anxious_preoccupied"], "valence": 0.0, "arousal": 0.0, "confidence": 0.8, "timestamp": "2025-09-17T15:52:46Z", "qa_id": "qa_pair_001", "session_id": "session_001"},
  {"chunk_id": "s001.qa_pair_001.c3", "text": "I do often use \u2018creative visualisation\u2019 to simulate emotions if it's going to serve a purpose. For example, in the gym when I\u2019m lifting weights, I will typically visualise something that would make me angry, as it \u2018feels\u2019 like it gives me extra strength. Friends have often said to me they saw me in the gym, but I walked right past them with a vacant look in my eyes, or one person hilariously described it as 'crazy eyes'! There's nothing crazy / angry figuratively however, it's just a side effect of me trying to disconnect so much visual brain-space to make room for the visualization. I literally never remember even seeing them.", "source": "therapy.md", "framework_tags": ["Emotion:Anger", "Defense:Dissociation", "Schema:Emotional_deprivation"], "valence": -0.5, "arousal": 0.7, "confidence": 0.8, "timestamp": "2025-09-17T15:52:46Z", "qa_id": "qa_pair_001", "session_id": "session_001"}

] AS c
OPTIONAL MATCH (q:QA_Pair {id: c.qa_id})
OPTIONAL MATCH (s:Session {session_id: c.session_id})
WITH c, q, s
MATCH (t:TextChunk {id: c.chunk_id})
FOREACH (_ IN CASE WHEN q IS NOT NULL THEN [1] ELSE [] END |
  MERGE (q)-[:HAS_CHUNK]->(t)
)
FOREACH (_ IN CASE WHEN s IS NOT NULL THEN [1] ELSE [] END |
  MERGE (s)-[:INCLUDES_CHUNK]->(t)
);

// Create framework relationships from chunks
UNWIND [
  {"chunk_id": "s001.qa_pair_001.c1", "text": "If I experience emotions directly about myself, they are under-stated to say the least. Rather it feels like I feel emotions through others, reflecting their feelings, or my perception of their feelings, opposed to having feelings about myself.", "source": "therapy.md", "framework_tags": ["Emotion:Empathy", "Attachment:Anxious_preoccupied"], "valence": 0.0, "arousal": 0.0, "confidence": 0.8, "timestamp": "2025-09-17T15:52:46Z", "qa_id": "qa_pair_001", "session_id": "session_001"},
  {"chunk_id": "s001.qa_pair_001.c2", "text": "If I\u2019m with someone who\u2019s happy, I feel happy. If I\u2019m with someone sad, I feel sad. I don\u2019t remember ever sitting around feeling sorry for myself, likewise I don\u2019t sit around feeling joy about myself.", "source": "therapy.md", "framework_tags": ["Emotion:Empathy", "Attachment:Anxious_preoccupied"], "valence": 0.0, "arousal": 0.0, "confidence": 0.8, "timestamp": "2025-09-17T15:52:46Z", "qa_id": "qa_pair_001", "session_id": "session_001"},
  {"chunk_id": "s001.qa_pair_001.c3", "text": "I do often use \u2018creative visualisation\u2019 to simulate emotions if it's going to serve a purpose. For example, in the gym when I\u2019m lifting weights, I will typically visualise something that would make me angry, as it \u2018feels\u2019 like it gives me extra strength. Friends have often said to me they saw me in the gym, but I walked right past them with a vacant look in my eyes, or one person hilariously described it as 'crazy eyes'! There's nothing crazy / angry figuratively however, it's just a side effect of me trying to disconnect so much visual brain-space to make room for the visualization. I literally never remember even seeing them.", "source": "therapy.md", "framework_tags": ["Emotion:Anger", "Defense:Dissociation", "Schema:Emotional_deprivation"], "valence": -0.5, "arousal": 0.7, "confidence": 0.8, "timestamp": "2025-09-17T15:52:46Z", "qa_id": "qa_pair_001", "session_id": "session_001"}

] AS c
UNWIND c.framework_tags AS tag
WITH c, SPLIT(tag, ':') AS parts
WITH c, parts[0] AS kind, parts[1] AS name
MATCH (t:TextChunk {id: c.chunk_id})

// Handle different framework types
FOREACH (_ IN CASE WHEN kind='Emotion' AND name IS NOT NULL THEN [1] ELSE [] END |
  MERGE (e:Emotion {name: toLower(name)})
  MERGE (t)-[:REVEALS_EMOTION {valence: c.valence, arousal: c.arousal, confidence: c.confidence}]->(e)
)

FOREACH (_ IN CASE WHEN kind='CognitiveDistortion' AND name IS NOT NULL THEN [1] ELSE [] END |
  MERGE (d:Cognitive_Distortion {type: toLower(name)})
  MERGE (t)-[:EXHIBITS_DISTORTION {confidence: c.confidence}]->(d)
)

FOREACH (_ IN CASE WHEN kind='Attachment' AND name IS NOT NULL THEN [1] ELSE [] END |
  MERGE (a:Attachment_Style {name: toLower(name)})
  MERGE (t)-[:REVEALS_ATTACHMENT_STYLE {confidence: c.confidence}]->(a)
)

FOREACH (_ IN CASE WHEN kind='Defense' AND name IS NOT NULL THEN [1] ELSE [] END |
  MERGE (m:Defense_Mechanism {name: toLower(name)})
  MERGE (t)-[:USES_DEFENSE_MECHANISM {confidence: c.confidence}]->(m)
)

FOREACH (_ IN CASE WHEN kind='Schema' AND name IS NOT NULL THEN [1] ELSE [] END |
  MERGE (s:Schema {name: toLower(name)})
  MERGE (t)-[:REVEALS_SCHEMA {confidence: c.confidence}]->(s)
)

FOREACH (_ IN CASE WHEN kind='Erikson' AND name IS NOT NULL THEN [1] ELSE [] END |
  MERGE (es:Erikson_Stage {name: toLower(name)})
  MERGE (t)-[:EXHIBITS_STAGE {confidence: c.confidence}]->(es)
);

// ============================================================================
// Created 3 TextChunk nodes with framework relationships
// ============================================================================