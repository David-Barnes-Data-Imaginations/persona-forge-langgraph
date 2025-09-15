
// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:09:26
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
MERGE (qa:QA_Pair {id: 'qa_pair_001', question: 'N/A', answer: 'N/A'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Empathy'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.2, arousal: 0.3, confidence: 0.8}]->(e1);
MERGE (e2:Emotion {name: 'Anger visualization'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.5, arousal: 0.7, confidence: 0.7}]->(e2);
MERGE (e3:Emotion {name: 'Sadness when others sad'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.4, confidence: 0.7}]->(e3);
MERGE (cd:Cognitive_Distortion {type: 'Rationalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd);
MERGE (es:Erikson_Stage {stage: 'Identity vs role confusion'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.7}]->(es);
MERGE (as:Attachment_Style {style: 'Anxious preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.6, extraversion: 0.4, agreeableness: 0.5, neuroticism: 0.5, confidence: 0.7}]->(bf);
MERGE (sch:Schema {name: 'Emotional deprivation'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch);
MERGE (dm1:Defense_Mechanism {name: 'Denial'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm1);
MERGE (dm2:Defense_Mechanism {name: 'Intellectualization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm2);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:12:13
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
MERGE (qa:QA_Pair {id: 'qa_pair_002'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Calm'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.2, arousal: 0.1, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Detached'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.1, arousal: 0.05, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Self‑assertive'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.3, arousal: 0.15, confidence: 0.7}]->(e3);
MERGE (e4:Emotion {name: 'Altruistic'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.25, arousal: 0.1, confidence: 0.7}]->(e4);
MERGE (cd1:Cognitive_Distortion {type: 'Minimization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'All or nothing thinking'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd2);
MERGE (es:Erikson_Stage {stage: 'Intimacy vs isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.7}]->(es);
MERGE (as:Attachment_Style {style: 'Dismissive avoidant'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (dm1:Defense_Mechanism {mechanism: 'Denial'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm1);
MERGE (dm2:Defense_Mechanism {mechanism: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm2);
MERGE (sch:Schema {name: 'Self‑sacrifice'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.8, extraversion: 0.3, agreeableness: 0.7, neuroticism: 0.2, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:13:23
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
MERGE (qa:QA_Pair {id: 'qa_pair_003', question: '', answer: ''});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Calm Detachment'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.2, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Emotional Exhaustion'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.7, arousal: 0.8, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Neutral Detachment'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.0, arousal: 0.1, confidence: 0.8}]->(e3);
MERGE (e4:Emotion {name: 'Anxiety in Social Context'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.5, confidence: 0.7}]->(e4);
MERGE (cd1:Cognitive_Distortion {type: 'Labeling'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'Personalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);
MERGE (es:Erikson_Stage {stage: 'Generativity vs stagnation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {style: 'Anxious preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);
MERGE (dm:Defense_Mechanism {mechanism: 'Suppression'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.8}]->(dm);
MERGE (sch:Schema {schema: 'Defectiveness shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.7, extraversion: 0.4, agreeableness: 0.6, neuroticism: 0.7, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:16:00
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_004', question: '', answer: ''});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Enthusiasm'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.8, arousal: 0.7, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.2, arousal: 0.3, confidence: 0.6}]->(e2);
MERGE (es:Erikson_Stage {stage: 'initiative_vs_guilt'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.7}]->(es);
MERGE (as:Attachment_Style {style: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (bf:Big_Five {profile: 'custom'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.9, conscientiousness: 0.6, extraversion: 0.7, agreeableness: 0.6, neuroticism: 0.3, confidence: 0.8}]->(bf);

// ============================================================================


// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:16:49
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_005', question: 'N/A', answer: 'N/A'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Enthusiasm'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.8, arousal: 0.7, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.2, arousal: 0.3, confidence: 0.6}]->(e2);
MERGE (es:Erikson_Stage {stage: 'Initiative_vs_guilt'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.7}]->(es);
MERGE (as:Attachment_Style {style: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.9, conscientiousness: 0.6, extraversion: 0.7, agreeableness: 0.6, neuroticism: 0.3, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:17:06
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
MERGE (qa:QA_Pair {id: 'qa_pair_006'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Empathy'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.4, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Fulfillment'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.8, arousal: 0.3, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Amusement'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.2, confidence: 0.7}]->(e3);
MERGE (es:Erikson_Stage {stage: 'intimacy_vs_isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {style: 'secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.6, extraversion: 0.5, agreeableness: 0.8, neuroticism: 0.3, confidence: 0.8}]->(bf);

// ============================================================================
=
// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:17:54
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
MERGE (qa:QA_Pair {id: 'qa_pair_007', question: '', answer: ''});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Amusement'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.4, confidence: 0.8}]->(e1);
MERGE (e2:Emotion {name: 'Self‑deprecation'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.5, confidence: 0.7}]->(e2);
MERGE (e3:Emotion {name: 'Pride'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.5, arousal: 0.3, confidence: 0.7}]->(e3);
MERGE (e4:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.6, confidence: 0.6}]->(e4);
MERGE (cd1:Cognitive_Distortion {type: 'Overgeneralization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'Emotional reasoning'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);
MERGE (es:Erikson_Stage {stage: 'Identity vs role confusion'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {style: 'Anxious preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.9, conscientiousness: 0.5, extraversion: 0.6, agreeableness: 0.4, neuroticism: 0.7, confidence: 0.7}]->(bf);
MERGE (sc:Schema {name: 'Defectiveness shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sc);
MERGE (dm:Defense_Mechanism {mechanism: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:18:28
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
MERGE (qa:QA_Pair {id: 'qa_pair_008', question: 'N/A', answer: 'N/A'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Curiosity'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.7, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Pride'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.5, arousal: 0.5, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.3, arousal: 0.6, confidence: 0.7}]->(e3);
MERGE (cd1:Cognitive_Distortion {type: 'Labeling'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'Should statements'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);
MERGE (es:Erikson_Stage {stage: 'Identity vs role confusion'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {style: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (dm:Defense_Mechanism {mechanism: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm);
MERGE (sch:Schema {name: 'Approval seeking'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.9, conscientiousness: 0.8, extraversion: 0.5, agreeableness: 0.8, neuroticism: 0.4, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:19:16
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
MERGE (qa:QA_Pair {id: 'qa_pair_009'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Pride'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.4, confidence: 0.8}]->(e1);
MERGE (e2:Emotion {name: 'Humor'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.3, confidence: 0.7}]->(e2);
MERGE (e3:Emotion {name: 'Self‑deprecation'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.2, confidence: 0.6}]->(e3);
MERGE (e4:Emotion {name: 'Protective motivation'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.5, arousal: 0.3, confidence: 0.7}]->(e4);
MERGE (cd1:Cognitive_Distortion {type: 'Personalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'Should statements'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd2);
MERGE (es:Erikson_Stage {stage: 'Generativity_vs_stagnation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {style: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (dm:Defense_Mechanism {mechanism: 'Humor (intellectualization)'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm);
MERGE (sch1:Schema {name: 'Self‑sacrifice'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch1);
MERGE (sch2:Schema {name: 'Approval seeking'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch2);
MERGE (bf:Big_Five {profile: 'qa_pair_009'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.7, extraversion: 0.5, agreeableness: 0.7, neuroticism: 0.4, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:19:41
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_010', question: 'Analysis Entry #10', answer: 'The client reflects on a vivid, imaginative childhood that shaped a strong sense of identity and purpose. The narrative is largely positive, highlighting pride in training and role models, yet interspersed with self‑deprecating remarks that suggest a tendency to minimize personal achievements. Cognitive distortions such as minimization and all‑or‑nothing thinking are evident. The client appears to have a secure attachment base, supported by parental permissiveness and mentorship. Personality analysis indicates high openness and conscientiousness, moderate extraversion and agreeableness, and low neuroticism, suggesting a disciplined, creative individual who may occasionally undervalue their own accomplishments.'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Nostalgia'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.4, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Pride'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.5, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Self‑deprecation'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.3, confidence: 0.8}]->(e3);
MERGE (e4:Emotion {name: 'Anxiety about judgment'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.4, confidence: 0.7}]->(e4);
MERGE (cd1:Cognitive_Distortion {type: 'Minimization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'All or nothing thinking'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd2);
MERGE (es:Erikson_Stage {stage: 'Identity vs role confusion'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.9}]->(es);
MERGE (as:Attachment_Style {style: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (dm:Defense_Mechanism {mechanism: 'Minimization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.8}]->(dm);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.9, extraversion: 0.5, agreeableness: 0.7, neuroticism: 0.4, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:20:06
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_011', question: '...', answer: '...'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.8, arousal: 0.9, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Relief'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.4, confidence: 0.7}]->(e2);
MERGE (e3:Emotion {name: 'Frustration'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.6, confidence: 0.6}]->(e3);
MERGE (e4:Emotion {name: 'Hope'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.4, arousal: 0.3, confidence: 0.5}]->(e4);
MERGE (cd1:Cognitive_Distortion {type: 'Personalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'Emotional reasoning'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);
MERGE (cd3:Cognitive_Distortion {type: 'Overgeneralization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd3);
MERGE (es:Erikson_Stage {stage: 'Identity vs role confusion'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.7}]->(es);
MERGE (as:Attachment_Style {style: 'Anxious preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (dm:Defense_Mechanism {mechanism: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.8}]->(dm);
MERGE (sch:Schema {schema: 'Self‑sacrifice'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.7, extraversion: 0.4, agreeableness: 0.7, neuroticism: 0.9, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:21:08
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_012', question: 'N/A', answer: 'N/A'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Enthusiasm'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.8, arousal: 0.5, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Confidence'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.4, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Humor'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.3, confidence: 0.7}]->(e3);
MERGE (e4:Emotion {name: 'Calm'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.5, arousal: 0.2, confidence: 0.8}]->(e4);
MERGE (cd1:Cognitive_Distortion {type: 'Minimization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'Rationalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd2);
MERGE (es:Erikson_Stage {stage: 'Generativity_vs_stagnation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {style: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (dm1:Defense_Mechanism {name: 'Humor'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.8}]->(dm1);
MERGE (dm2:Defense_Mechanism {name: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm2);
MERGE (dm3:Defense_Mechanism {name: 'Intellectualization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm3);
MERGE (sc:Schema {name: 'Approval_seeking'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sc);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.9, extraversion: 0.6, agreeableness: 0.8, neuroticism: 0.3, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:21:44
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_013', question: 'Analysis Entry #13', answer: 'The client displays a strong orientation toward objective service and detachment, which yields contentment and determination. However, the same detachment creates anxiety about burnout and self‑criticism, reflecting all‑or‑nothing and catastrophizing distortions. The focus on generativity and service aligns with Erikson’s generativity stage, while anxious preoccupied attachment and emotional inhibition suggest a need for supportive self‑care. Intellectualization and suppression serve as defense mechanisms to manage emotional intensity. High openness and conscientiousness support creative problem‑solving, but moderate neuroticism indicates vulnerability to stress. Overall, the client balances a constructive, service‑oriented identity with underlying anxieties about self‑worth and burnout.'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'contentment'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.4, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.6, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'determination'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.5, confidence: 0.8}]->(e3);
MERGE (e4:Emotion {name: 'self_criticism'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.5, confidence: 0.7}]->(e4);
MERGE (cd1:Cognitive_Distortion {type: 'all_or_nothing_thinking'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'catastrophizing'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd2);
MERGE (cd3:Cognitive_Distortion {type: 'emotional_reasoning'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd3);
MERGE (es:Erikson_Stage {stage: 'generativity_vs_stagnation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {style: 'anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);
MERGE (dm1:Defense_Mechanism {mechanism: 'intellectualization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.8}]->(dm1);
MERGE (dm2:Defense_Mechanism {mechanism: 'suppression'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm2);
MERGE (sc1:Schema {name: 'vulnerability_to_harm'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sc1);
MERGE (sc2:Schema {name: 'emotional_inhibition'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sc2);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.8, extraversion: 0.4, agreeableness: 0.7, neuroticism: 0.6, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:32:19
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
MERGE (qa:QA_Pair {id: 'qa_pair_014'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e:Emotion {name: 'enthusiasm'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.8, arousal: 0.6, confidence: 0.9}]->(e);
MERGE (es:Erikson_Stage {stage: 'identity_vs_role_confusion'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.7}]->(es);
MERGE (as:Attachment_Style {style: 'secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.9, conscientiousness: 0.8, extraversion: 0.5, agreeableness: 0.7, neuroticism: 0.3, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:32:53
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_015'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e:Emotion {name: 'Optimism'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.4, confidence: 0.9}]->(e);
MERGE (cd1:Cognitive_Distortion {type: 'Overgeneralization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'Minimization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);
MERGE (es:Erikson_Stage {stage: 'Industry_vs_inferiority'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {style: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.9, conscientiousness: 0.7, extraversion: 0.4, agreeableness: 0.5, neuroticism: 0.3, confidence: 0.8}]->(bf);
MERGE (dm1:Defense_Mechanism {mechanism: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm1);
MERGE (dm2:Defense_Mechanism {mechanism: 'Intellectualization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm2);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:33:22
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
MERGE (qa:QA_Pair {id: 'qa_pair_016', question: '...', answer: '...'});
CREATE (c)-[:PARTICIPATED_IN]->(s);
CREATE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Anger'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.8, arousal: 0.9, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Frustration'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.7, arousal: 0.8, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.6, arousal: 0.8, confidence: 0.8}]->(e3);
MERGE (e4:Emotion {name: 'Distrust'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.6, arousal: 0.7, confidence: 0.7}]->(e4);
MERGE (cd1:Cognitive_Distortion {type: 'Catastrophizing'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'Overgeneralization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);
MERGE (cd3:Cognitive_Distortion {type: 'Personalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd3);
MERGE (cd4:Cognitive_Distortion {type: 'Mind_reading'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd4);
MERGE (cd5:Cognitive_Distortion {type: 'Emotional_reasoning'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd5);
MERGE (es:Erikson_Stage {stage: 'Intimacy_vs_isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {style: 'Anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (dm1:Defense_Mechanism {mechanism: 'Denial'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm1);
MERGE (dm2:Defense_Mechanism {mechanism: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm2);
MERGE (sch1:Schema {name: 'Mistrust_abuse'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch1);
MERGE (sch2:Schema {name: 'Emotional_inhibition'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch2);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.9, conscientiousness: 0.6, extraversion: 0.7, agreeableness: 0.4, neuroticism: 0.8, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:39:54
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_017', question: '...', answer: '...'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.8, arousal: 0.7, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'hope'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.4, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'sadness'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.6, arousal: 0.3, confidence: 0.7}]->(e3);
MERGE (cd1:Cognitive_Distortion {type: 'catastrophizing'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'all_or_nothing_thinking'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);
MERGE (cd3:Cognitive_Distortion {type: 'emotional_reasoning'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd3);
MERGE (es:Erikson_Stage {stage: 'identity_vs_role_confusion'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {style: 'anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.9, conscientiousness: 0.5, extraversion: 0.3, agreeableness: 0.6, neuroticism: 0.9, confidence: 0.8}]->(bf);
MERGE (sch1:Schema {name: 'defectiveness_shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch1);
MERGE (sch2:Schema {name: 'failure'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch2);
MERGE (dm:Defense_Mechanism {name: 'intellectualization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:40:08
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
MERGE (qa:QA_Pair {id: 'qa_pair_018', question: 'N/A', answer: 'N/A'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Calm'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: -0.4, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Empathy'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: -0.2, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Exhaustion'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.3, confidence: 0.7}]->(e3);
MERGE (e4:Emotion {name: 'Misunderstood'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.3, arousal: 0.2, confidence: 0.7}]->(e4);
MERGE (cd1:Cognitive_Distortion {type: 'Mind reading'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'Overgeneralization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);
MERGE (es:Erikson_Stage {stage: 'Integrity vs despair'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {style: 'Anxious preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (dm1:Defense_Mechanism {mechanism: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.8}]->(dm1);
MERGE (dm2:Defense_Mechanism {mechanism: 'Intellectualization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm2);
MERGE (sch1:Schema {name: 'Self-sacrifice'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch1);
MERGE (sch2:Schema {name: 'Emotional inhibition'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch2);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.7, extraversion: 0.3, agreeableness: 0.8, neuroticism: 0.5, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:40:39
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_019', question: 'Analysis', answer: ''});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);

MERGE (e1:Emotion {name: 'Empathy'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.4, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Guilt'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.7, arousal: 0.6, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Sadness'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.6, arousal: 0.5, confidence: 0.7}]->(e3);
MERGE (e4:Emotion {name: 'Relief'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.5, arousal: 0.3, confidence: 0.8}]->(e4);

MERGE (cd1:Cognitive_Distortion {type: 'Should statements'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'Personalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);
MERGE (cd3:Cognitive_Distortion {type: 'Emotional reasoning'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd3);
MERGE (cd4:Cognitive_Distortion {type: 'Catastrophizing'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.5}]->(cd4);

MERGE (es:Erikson_Stage {stage: 'intimacy_vs_isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);

MERGE (as:Attachment_Style {style: 'anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);

MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.8, extraversion: 0.4, agreeableness: 0.7, neuroticism: 0.8, confidence: 0.7}]->(bf);

MERGE (sch1:Schema {name: 'Self-sacrifice'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch1);
MERGE (sch2:Schema {name: 'Defectiveness shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch2);
MERGE (sch3:Schema {name: 'Approval seeking'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch3);

MERGE (dm1:Defense_Mechanism {name: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm1);
MERGE (dm2:Defense_Mechanism {name: 'Denial'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm2);
MERGE (dm3:Defense_Mechanism {name: 'Suppression'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm3);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:41:31
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
MERGE (qa:QA_Pair {id: 'qa_pair_020', question: '', answer: ''});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);

MERGE (e1:Emotion {name: 'Gratitude'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.5, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Sadness'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.6, arousal: 0.6, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Awe/Relief'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.4, confidence: 0.8}]->(e3);
MERGE (e4:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.5, confidence: 0.7}]->(e4);

MERGE (cd1:Cognitive_Distortion {type: 'Personalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'Emotional Reasoning'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);

MERGE (es:Erikson_Stage {stage: 'Identity_vs_Role_Confusion'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);

MERGE (as:Attachment_Style {style: 'Anxious_Preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);

MERGE (dm:Defense_Mechanism {name: 'Intellectualization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm);

MERGE (sch:Schema {name: 'Defectiveness_Shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch);

MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.7, extraversion: 0.5, agreeableness: 0.8, neuroticism: 0.7, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:41:54
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_021', question: '...', answer: '...'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'nostalgia'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.5, confidence: 0.8}]->(e1);
MERGE (e2:Emotion {name: 'gratitude'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.4, confidence: 0.7}]->(e2);
MERGE (e3:Emotion {name: 'sadness'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.6, confidence: 0.8}]->(e3);
MERGE (e4:Emotion {name: 'loneliness'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.5, confidence: 0.7}]->(e4);
MERGE (cd1:Cognitive_Distortion {type: 'emotional_reasoning'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'personalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);
MERGE (es:Erikson_Stage {stage: 'intimacy_vs_isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {style: 'anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (dm:Defense_Mechanism {mechanism: 'rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm);
MERGE (sch1:Schema {name: 'abandonment'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch1);
MERGE (sch2:Schema {name: 'social_isolation_alienation'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch2);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.6, extraversion: 0.5, agreeableness: 0.7, neuroticism: 0.7, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:42:52
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
MERGE (qa:QA_Pair {id: 'qa_pair_022'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Sadness'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.7, arousal: 0.5, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Frustration'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.6, arousal: 0.6, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Contentment'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.5, arousal: 0.3, confidence: 0.7}]->(e3);
MERGE (e4:Emotion {name: 'Melancholy'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.4, confidence: 0.8}]->(e4);
MERGE (cd1:Cognitive_Distortion {type: 'Overgeneralization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'Personalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);
MERGE (cd3:Cognitive_Distortion {type: 'Catastrophizing'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd3);
MERGE (es:Erikson_Stage {stage: 'Intimacy_vs_isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {style: 'Anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (dm:Defense_Mechanism {mechanism: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm);
MERGE (sch1:Schema {name: 'Abandonment'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch1);
MERGE (sch2:Schema {name: 'Defectiveness_shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch2);
MERGE (sch3:Schema {name: 'Social_isolation_alienation'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch3);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.7, extraversion: 0.4, agreeableness: 0.6, neuroticism: 0.8, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:44:31
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
MERGE (qa:QA_Pair {id: 'qa_pair_024', question: 'N/A', answer: 'N/A'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Boredom'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.3, arousal: 0.1, confidence: 0.8}]->(e1);
MERGE (e2:Emotion {name: 'Amusement'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.4, arousal: 0.2, confidence: 0.7}]->(e2);
MERGE (e3:Emotion {name: 'Contentment'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.3, arousal: 0.1, confidence: 0.6}]->(e3);
MERGE (cd:Cognitive_Distortion {type: 'Emotional reasoning'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd);
MERGE (es:Erikson_Stage {stage: 'Intimacy vs isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {style: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.6, conscientiousness: 0.5, extraversion: 0.4, agreeableness: 0.7, neuroticism: 0.3, confidence: 0.7}]->(bf);
MERGE (sch:Schema {name: 'Social isolation alienation'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch);
MERGE (dm:Defense_Mechanism {name: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:44:56
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_025'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Sadness'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.7, arousal: 0.5, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Loneliness'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.6, arousal: 0.4, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Frustration'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.6, confidence: 0.7}]->(e3);
MERGE (e4:Emotion {name: 'Nostalgia'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.4, arousal: 0.3, confidence: 0.6}]->(e4);
MERGE (cd1:Cognitive_Distortion {type: 'Overgeneralization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'Personalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);
MERGE (cd3:Cognitive_Distortion {type: 'Labeling'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd3);
MERGE (es:Erikson_Stage {stage: 'Intimacy_vs_isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.9}]->(es);
MERGE (as:Attachment_Style {style: 'Anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (dm1:Defense_Mechanism {mechanism: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm1);
MERGE (dm2:Defense_Mechanism {mechanism: 'Denial'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm2);
MERGE (sch1:Schema {schema: 'Abandonment'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch1);
MERGE (sch2:Schema {schema: 'Social_isolation_alienation'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch2);
MERGE (sch3:Schema {schema: 'Self-sacrifice'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch3);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.6, conscientiousness: 0.8, extraversion: 0.3, agreeableness: 0.5, neuroticism: 0.8, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:45:30
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_026', question: '', answer: ''});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.7, arousal: 0.6, confidence: 0.8}]->(e1);
MERGE (e2:Emotion {name: 'Resignation'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.4, confidence: 0.7}]->(e2);
MERGE (e3:Emotion {name: 'Self‑justification'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.0, arousal: 0.3, confidence: 0.6}]->(e3);
MERGE (cd1:Cognitive_Distortion {type: 'All or nothing thinking'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'Overgeneralization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);
MERGE (cd3:Cognitive_Distortion {type: 'Mind reading'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd3);
MERGE (cd4:Cognitive_Distortion {type: 'Personalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd4);
MERGE (es:Erikson_Stage {stage: 'Intimacy vs isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {style: 'Anxious preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);
MERGE (dm1:Defense_Mechanism {mechanism: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.8}]->(dm1);
MERGE (dm2:Defense_Mechanism {mechanism: 'Denial'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm2);
MERGE (dm3:Defense_Mechanism {mechanism: 'Projection'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.5}]->(dm3);
MERGE (sch1:Schema {name: 'Defectiveness shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch1);
MERGE (sch2:Schema {name: 'Self‑sacrifice'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch2);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.6, conscientiousness: 0.7, extraversion: 0.3, agreeableness: 0.5, neuroticism: 0.8, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:46:03
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa:QA_Pair {id: 'qa_pair_027'});
MERGE (e1:Emotion {name: 'Contentment'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.3, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Humor'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.4, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Frustration'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.5, confidence: 0.7}]->(e3);
MERGE (e4:Emotion {name: 'Self‑efficacy'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.8, arousal: 0.2, confidence: 0.9}]->(e4);
MERGE (cd1:Cognitive_Distortion {type: 'Overgeneralization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'Labeling'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);
MERGE (es:Erikson_Stage {stage: 'Industry vs Inferiority'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {style: 'Anxious preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);
MERGE (dm1:Defense_Mechanism {mechanism: 'Humor'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.8}]->(dm1);
MERGE (dm2:Defense_Mechanism {mechanism: 'Avoidance'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm2);
MERGE (sch:Schema {name: 'Defectiveness shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.8, extraversion: 0.5, agreeableness: 0.6, neuroticism: 0.5, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:46:50
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
MERGE (qa:QA_Pair {id: 'qa_pair_028'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Enthusiasm'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.9, arousal: 0.7, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Calm'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.8, arousal: 0.2, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Sociability'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.6, confidence: 0.8}]->(e3);
MERGE (es:Erikson_Stage {stage: 'identity_vs_role_confusion'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.7}]->(es);
MERGE (as:Attachment_Style {style: 'anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (dm:Defense_Mechanism {mechanism: 'rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm);
MERGE (sc:Schema {name: 'approval_seeking'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sc);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 1.0, conscientiousness: 1.0, extraversion: 0.57, agreeableness: 1.0, neuroticism: 0.14, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:47:16
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_029', question: '', answer: ''});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'contentment'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.4, confidence: 0.8}]->(e1);
MERGE (e2:Emotion {name: 'determination'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.6, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'guilt'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.5, confidence: 0.7}]->(e3);
MERGE (e4:Emotion {name: 'anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.5, confidence: 0.7}]->(e4);
MERGE (cd:Cognitive_Distortion {type: 'rationalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd);
MERGE (es:Erikson_Stage {stage: 'intimacy_vs_isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {style: 'anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);
MERGE (dm:Defense_Mechanism {mechanism: 'rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.8}]->(dm);
MERGE (sch:Schema {name: 'self_sacrifice'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.8, extraversion: 0.5, agreeableness: 0.8, neuroticism: 0.5, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:47:41
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_030', question: 'Analysis Entry #30', answer: 'The client displays a pronounced threat‑driven arousal pattern marked by anger, frustration, and anxiety, often managed through suppression and avoidance. Their low mood states are tied to empathy for suffering and intentional sleep deprivation to control idea flow. Attachment analysis points to anxious preoccupation, with a reliance on external cues (music, visualizations) to regulate affect. Schema work may focus on emotional inhibition and vulnerability to harm. High openness and conscientiousness suggest creative and organized tendencies, while elevated neuroticism indicates emotional volatility. This profile highlights a need for emotion regulation strategies that address both hyperarousal and empathic distress.'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'anger'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.7, arousal: 0.8, confidence: 0.8}]->(e1);
MERGE (e2:Emotion {name: 'frustration'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.6, arousal: 0.7, confidence: 0.7}]->(e2);
MERGE (e3:Emotion {name: 'sadness'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.8, arousal: 0.3, confidence: 0.8}]->(e3);
MERGE (e4:Emotion {name: 'anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.6, confidence: 0.7}]->(e4);
MERGE (cd1:Cognitive_Distortion {type: 'jumping_to_conclusions'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'overgeneralization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd2);
MERGE (es:Erikson_Stage {stage: 'intimacy_vs_isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.7}]->(es);
MERGE (as:Attachment_Style {style: 'anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);
MERGE (dm1:Defense_Mechanism {mechanism: 'suppression'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm1);
MERGE (dm2:Defense_Mechanism {mechanism: 'avoidance'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm2);
MERGE (sch1:Schema {name: 'emotional_inhibition'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch1);
MERGE (sch2:Schema {name: 'vulnerability_to_harm'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch2);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.7, extraversion: 0.4, agreeableness: 0.6, neuroticism: 0.8, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:48:25
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
MERGE (qa:QA_Pair {id: 'qa_pair_031'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Contentment'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.4, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Motivation'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.8, arousal: 0.5, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Calm'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.3, confidence: 0.8}]->(e3);
MERGE (e4:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.6, confidence: 0.7}]->(e4);
MERGE (es:Erikson_Stage {stage: 'Autonomy_vs_shame/doubt'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {style: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (bf:Big_Five {openness: 0.8, conscientiousness: 0.6, extraversion: 0.5, agreeableness: 0.7, neuroticism: 0.3, confidence: 0.8});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.6, extraversion: 0.5, agreeableness: 0.7, neuroticism: 0.3, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:49:06
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_032', question: '', answer: ''});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Contentment'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.4, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Motivation'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.8, arousal: 0.5, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Calm'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.3, confidence: 0.8}]->(e3);
MERGE (e4:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.6, confidence: 0.7}]->(e4);
MERGE (es:Erikson_Stage {stage: 'Autonomy vs shame/doubt'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {style: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.6, extraversion: 0.5, agreeableness: 0.7, neuroticism: 0.3, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:50:08
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
MERGE (qa:QA_Pair {id: 'qa_pair_033', question: 'N/A', answer: 'N/A'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Contentment'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.4, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Motivation'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.8, arousal: 0.5, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Calm'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.3, confidence: 0.8}]->(e3);
MERGE (e4:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.6, confidence: 0.7}]->(e4);
MERGE (es:Erikson_Stage {stage: 'autonomy_vs_shame_doubt'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {style: 'secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.6, extraversion: 0.5, agreeableness: 0.7, neuroticism: 0.3, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:50:29
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_034'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e:Emotion {name: 'negative_valence'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.6, confidence: 0.8}]->(e);
MERGE (cd:Cognitive_Distortion {type: 'magnification'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd);
MERGE (es:Erikson_Stage {stage: 'industry_vs_inferiority'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.5}]->(es);
MERGE (as:Attachment_Style {style: 'anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.5, conscientiousness: 0.7, extraversion: 0.4, agreeableness: 0.6, neuroticism: 0.7, confidence: 0.7}]->(bf);
MERGE (sch:Schema {name: 'defectiveness_shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:51:29
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
MERGE (qa:QA_Pair {id: 'qa_pair_035', question: '', answer: ''});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.7, confidence: 0.8}]->(e1);
MERGE (e2:Emotion {name: 'sadness'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.6, arousal: 0.5, confidence: 0.7}]->(e2);
MERGE (e3:Emotion {name: 'relief'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.5, arousal: 0.3, confidence: 0.7}]->(e3);
MERGE (e4:Emotion {name: 'negative_valence'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.6, confidence: 0.8}]->(e4);
MERGE (cd:Cognitive_Distortion {type: 'magnification'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd);
MERGE (es:Erikson_Stage {stage: 'industry_vs_inferiority'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.5}]->(es);
MERGE (as:Attachment_Style {style: 'anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.5, conscientiousness: 0.7, extraversion: 0.4, agreeableness: 0.6, neuroticism: 0.7, confidence: 0.7}]->(bf);
MERGE (sch:Schema {name: 'defectiveness_shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:52:02
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_036', question: 'N/A', answer: 'N/A'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Frustration'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.7, arousal: 0.6, confidence: 0.8}]->(e1);
MERGE (e2:Emotion {name: 'Disappointment'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.6, arousal: 0.5, confidence: 0.7}]->(e2);
MERGE (e3:Emotion {name: 'Relief'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.4, arousal: 0.3, confidence: 0.6}]->(e3);
MERGE (e4:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.7, confidence: 0.7}]->(e4);
MERGE (cd1:Cognitive_Distortion {type: 'All or nothing thinking'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'Catastrophizing'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd2);
MERGE (cd3:Cognitive_Distortion {type: 'Overgeneralization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.5}]->(cd3);
MERGE (es:Erikson_Stage {stage: 'Identity vs role confusion'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.7}]->(es);
MERGE (as:Attachment_Style {style: 'Anxious preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.6}]->(as);
MERGE (dm:Defense_Mechanism {mechanism: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm);
MERGE (sch1:Schema {name: 'Defectiveness shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch1);
MERGE (sch2:Schema {name: 'Failure'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch2);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.6, conscientiousness: 0.4, extraversion: 0.5, agreeableness: 0.5, neuroticism: 0.7, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 18:52:29
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
MERGE (qa:QA_Pair {id: 'qa_pair_037'});
MERGE (c)-[:PARTICIPATED_IN]->(s);
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Frustration'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.5, confidence: 0.8}]->(e1);
MERGE (e2:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.6, confidence: 0.9}]->(e2);
MERGE (e3:Emotion {name: 'Relief'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.3, arousal: 0.4, confidence: 0.7}]->(e3);
MERGE (e4:Emotion {name: 'Confusion'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.2, arousal: 0.3, confidence: 0.7}]->(e4);
MERGE (cd1:Cognitive_Distortion {type: 'Catastrophizing'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'Overgeneralization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);
MERGE (cd3:Cognitive_Distortion {type: 'Personalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd3);
MERGE (es:Erikson_Stage {stage: 'Industry vs Inferiority'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {style: 'Anxious preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (dm:Defense_Mechanism {mechanism: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm);
MERGE (sc:Schema {name: 'Emotional deprivation'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sc);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.9, extraversion: 0.5, agreeableness: 0.6, neuroticism: 0.8, confidence: 0.8}]->(bf);

// ============================================================================
