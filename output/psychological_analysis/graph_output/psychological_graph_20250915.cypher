
// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:14:50
// ============================================================================

MERGE (c:Client {id: 'client_001'});
MERGE (s:Session {session_id: 'session_001'});
MERGE (c)-[:PARTICIPATED_IN]->(s);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:15:25
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_001'});
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Empathy'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.2, arousal: 0.3, confidence: 0.8}]->(e1);
MERGE (e2:Emotion {name: 'Anger visualization'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.5, arousal: 0.7, confidence: 0.7}]->(e2);
MERGE (e3:Emotion {name: 'Sadness when others sad'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.4, confidence: 0.7}]->(e3);
MERGE (cd:Cognitive_Distortion {type: 'Rationalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd);
MERGE (es:Erikson_Stage {name: 'Identity vs role confusion'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.7}]->(es);
MERGE (as:Attachment_Style {name: 'Anxious preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);
MERGE (dm1:Defense_Mechanism {name: 'Denial'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm1);
MERGE (dm2:Defense_Mechanism {name: 'Intellectualization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm2);
MERGE (sch:Schema {name: 'Emotional deprivation'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.6, extraversion: 0.4, agreeableness: 0.5, neuroticism: 0.5, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:16:04
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_002'});
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

MERGE (es:Erikson_Stage {name: 'Intimacy vs isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.7}]->(es);

MERGE (as:Attachment_Style {name: 'Dismissive avoidant'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);

MERGE (dm1:Defense_Mechanism {name: 'Denial'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm1);
MERGE (dm2:Defense_Mechanism {name: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm2);

MERGE (sch:Schema {name: 'Self‑sacrifice'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch);

MERGE (bf:Big_Five {profile: 'qa_pair_002_profile'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.8, extraversion: 0.3, agreeableness: 0.7, neuroticism: 0.2, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:16:37
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_003'});
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

MERGE (es:Erikson_Stage {name: 'Generativity_vs_stagnation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);

MERGE (as:Attachment_Style {name: 'Anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);

MERGE (dm:Defense_Mechanism {name: 'Suppression'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.8}]->(dm);

MERGE (sch:Schema {name: 'Defectiveness_shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch);

MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.7, extraversion: 0.4, agreeableness: 0.6, neuroticism: 0.7, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:16:54
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_004'});
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Enthusiasm'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.8, arousal: 0.7, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.2, arousal: 0.3, confidence: 0.6}]->(e2);
MERGE (es:Erikson_Stage {name: 'Initiative_vs_guilt'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.7}]->(es);
MERGE (as:Attachment_Style {name: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.9, conscientiousness: 0.6, extraversion: 0.7, agreeableness: 0.6, neuroticism: 0.3, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:17:18
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_005'});
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Enthusiasm'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.8, arousal: 0.7, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.2, arousal: 0.3, confidence: 0.6}]->(e2);
MERGE (es:Erikson_Stage {name: 'initiative_vs_guilt'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.7}]->(es);
MERGE (as:Attachment_Style {name: 'secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.9, conscientiousness: 0.6, extraversion: 0.7, agreeableness: 0.6, neuroticism: 0.3, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:17:48
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_006'});
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Empathy'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.4, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Fulfillment'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.8, arousal: 0.3, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Amusement'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.2, confidence: 0.7}]->(e3);
MERGE (es:Erikson_Stage {name: 'Intimacy_vs_isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {name: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.6, extraversion: 0.5, agreeableness: 0.8, neuroticism: 0.3, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:19:09
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_007'});
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Amusement'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.4, confidence: 0.8}]->(e1);
MERGE (e2:Emotion {name: 'Self_deprecation'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.5, confidence: 0.7}]->(e2);
MERGE (e3:Emotion {name: 'Pride'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.5, arousal: 0.3, confidence: 0.7}]->(e3);
MERGE (e4:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.6, confidence: 0.6}]->(e4);
MERGE (cd1:Cognitive_Distortion {type: 'Overgeneralization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'Emotional_reasoning'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);
MERGE (es:Erikson_Stage {name: 'Identity_vs_role_confusion'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {name: 'Anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);
MERGE (dm:Defense_Mechanism {name: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm);
MERGE (sch:Schema {name: 'Defectiveness_shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.9, conscientiousness: 0.5, extraversion: 0.6, agreeableness: 0.4, neuroticism: 0.7, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:20:03
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_008'});
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
MERGE (es:Erikson_Stage {name: 'Identity_vs_role_confusion'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {name: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (dm:Defense_Mechanism {name: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm);
MERGE (sch:Schema {name: 'Approval_seeking'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.9, conscientiousness: 0.8, extraversion: 0.5, agreeableness: 0.8, neuroticism: 0.4, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:20:33
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_009'});
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

MERGE (es:Erikson_Stage {name: 'Generativity vs stagnation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);

MERGE (as:Attachment_Style {name: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);

MERGE (dm:Defense_Mechanism {name: 'Humor (intellectualization)'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm);

MERGE (sch1:Schema {name: 'Self‑sacrifice'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch1);

MERGE (sch2:Schema {name: 'Approval seeking'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch2);

MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.7, extraversion: 0.5, agreeableness: 0.7, neuroticism: 0.4, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:21:00
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_010'});
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

MERGE (es:Erikson_Stage {name: 'Identity vs role confusion'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.9}]->(es);

MERGE (as:Attachment_Style {name: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);

MERGE (dm:Defense_Mechanism {name: 'Minimization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.8}]->(dm);

MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.9, extraversion: 0.5, agreeableness: 0.7, neuroticism: 0.4, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:21:23
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_011'});
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

MERGE (es:Erikson_Stage {name: 'Identity_vs_role_confusion'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.7}]->(es);

MERGE (as:Attachment_Style {name: 'Anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);

MERGE (dm:Defense_Mechanism {name: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.8}]->(dm);

MERGE (sch:Schema {name: 'Self-sacrifice'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch);

MERGE (bf:Big_Five {profile: 'qa_pair_011'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.7, extraversion: 0.4, agreeableness: 0.7, neuroticism: 0.9, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:21:57
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_012'});
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
MERGE (es:Erikson_Stage {name: 'Generativity_vs_stagnation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {name: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (dm1:Defense_Mechanism {name: 'Humor'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.8}]->(dm1);
MERGE (dm2:Defense_Mechanism {name: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm2);
MERGE (dm3:Defense_Mechanism {name: 'Intellectualization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm3);
MERGE (sch:Schema {name: 'Approval_seeking'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.9, extraversion: 0.6, agreeableness: 0.8, neuroticism: 0.3, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:22:35
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_013'});
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Contentment'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.4, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.6, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Determination'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.5, confidence: 0.8}]->(e3);
MERGE (e4:Emotion {name: 'Self-criticism'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.5, confidence: 0.7}]->(e4);
MERGE (cd1:Cognitive_Distortion {type: 'All or nothing thinking'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'Catastrophizing'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd2);
MERGE (cd3:Cognitive_Distortion {type: 'Emotional reasoning'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd3);
MERGE (es:Erikson_Stage {name: 'Generativity vs stagnation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {name: 'Anxious preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);
MERGE (dm1:Defense_Mechanism {name: 'Intellectualization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.8}]->(dm1);
MERGE (dm2:Defense_Mechanism {name: 'Suppression'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm2);
MERGE (sch1:Schema {name: 'Vulnerability to harm'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch1);
MERGE (sch2:Schema {name: 'Emotional inhibition'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch2);
MERGE (bf:Big_Five {profile: 'qa_pair_013'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.8, extraversion: 0.4, agreeableness: 0.7, neuroticism: 0.6, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:23:05
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_014'});
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e:Emotion {name: 'Enthusiasm'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.8, arousal: 0.6, confidence: 0.9}]->(e);
MERGE (es:Erikson_Stage {name: 'Identity_vs_role_confusion'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.7}]->(es);
MERGE (as:Attachment_Style {name: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.9, conscientiousness: 0.8, extraversion: 0.5, agreeableness: 0.7, neuroticism: 0.3, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:23:22
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_015'});
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e:Emotion {name: 'Optimism'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.4, confidence: 0.9}]->(e);
MERGE (cd1:Cognitive_Distortion {type: 'Overgeneralization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'Minimization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);
MERGE (es:Erikson_Stage {name: 'Industry vs inferiority'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {name: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);
MERGE (dm1:Defense_Mechanism {name: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm1);
MERGE (dm2:Defense_Mechanism {name: 'Intellectualization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm2);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.9, conscientiousness: 0.7, extraversion: 0.4, agreeableness: 0.5, neuroticism: 0.3, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:24:02
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_016'});
MERGE (s)-[:INCLUDES]->(qa);
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
MERGE (cd4:Cognitive_Distortion {type: 'Mind reading'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd4);
MERGE (cd5:Cognitive_Distortion {type: 'Emotional reasoning'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd5);
MERGE (es:Erikson_Stage {name: 'Intimacy vs isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {name: 'Anxious preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (dm1:Defense_Mechanism {name: 'Denial'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm1);
MERGE (dm2:Defense_Mechanism {name: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm2);
MERGE (sch1:Schema {name: 'Mistrust abuse'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch1);
MERGE (sch2:Schema {name: 'Emotional inhibition'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch2);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.9, conscientiousness: 0.6, extraversion: 0.7, agreeableness: 0.4, neuroticism: 0.8, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:25:10
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_017'});
MERGE (s)-[:INCLUDES]->(qa);

MERGE (e1:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.8, arousal: 0.7, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Hope'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.4, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Sadness'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.6, arousal: 0.3, confidence: 0.7}]->(e3);

MERGE (cd1:Cognitive_Distortion {type: 'Catastrophizing'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'All_or_nothing_thinking'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);
MERGE (cd3:Cognitive_Distortion {type: 'Emotional_reasoning'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd3);

MERGE (es:Erikson_Stage {name: 'Identity_vs_role_confusion'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);

MERGE (as:Attachment_Style {name: 'Anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);

MERGE (dm:Defense_Mechanism {name: 'Intellectualization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm);

MERGE (sch1:Schema {name: 'Defectiveness_shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch1);
MERGE (sch2:Schema {name: 'Failure'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch2);

MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.9, conscientiousness: 0.5, extraversion: 0.3, agreeableness: 0.6, neuroticism: 0.9, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:39:38
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_018'});
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

MERGE (es:Erikson_Stage {name: 'Integrity_vs_despair'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);

MERGE (as:Attachment_Style {name: 'Anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);

MERGE (dm1:Defense_Mechanism {name: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.8}]->(dm1);

MERGE (dm2:Defense_Mechanism {name: 'Intellectualization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm2);

MERGE (sch1:Schema {name: 'Self-sacrifice'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch1);

MERGE (sch2:Schema {name: 'Emotional_inhibition'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch2);

MERGE (bf:Big_Five {profile: 'qa_pair_018'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.7, extraversion: 0.3, agreeableness: 0.8, neuroticism: 0.5, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:40:20
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_019'});
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
MERGE (es:Erikson_Stage {name: 'Intimacy vs isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {name: 'Anxious preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (bf:Big_Five {profile: 'qa_pair_019'});
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
// CYPHER ENTRY - 2025-09-15 23:41:04
// ============================================================================

MATCH (s:Session {session_id: 'session_001'}); CREATE (qa:QA_Pair {id: 'qa_pair_020'});
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e_gratitude:Emotion {name: 'Gratitude'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.5, confidence: 0.9}]->(e_gratitude);
MERGE (e_sadness:Emotion {name: 'Sadness'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.6, arousal: 0.6, confidence: 0.8}]->(e_sadness);
MERGE (e_awe:Emotion {name: 'Awe/Relief'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.4, confidence: 0.8}]->(e_awe);
MERGE (e_anxiety:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.5, confidence: 0.7}]->(e_anxiety);
MERGE (cd_personalization:Cognitive_Distortion {type: 'Personalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd_personalization);
MERGE (cd_emotional_reasoning:Cognitive_Distortion {type: 'Emotional Reasoning'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd_emotional_reasoning);
MERGE (es_identity:Erikson_Stage {name: 'Identity vs Role Confusion'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es_identity);
MERGE (as_anxious:Attachment_Style {name: 'Anxious Preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as_anxious);
MERGE (dm_intellectualization:Defense_Mechanism {name: 'Intellectualization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm_intellectualization);
MERGE (sch_defectiveness:Schema {name: 'Defectiveness/ Shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch_defectiveness);
MERGE (bf:Big_Five {profile: 'qa_pair_020'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.7, extraversion: 0.5, agreeableness: 0.8, neuroticism: 0.7, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:41:31
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_021'});
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Nostalgia'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.5, confidence: 0.8}]->(e1);
MERGE (e2:Emotion {name: 'Gratitude'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.4, confidence: 0.7}]->(e2);
MERGE (e3:Emotion {name: 'Sadness'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.6, confidence: 0.8}]->(e3);
MERGE (e4:Emotion {name: 'Loneliness'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.5, confidence: 0.7}]->(e4);
MERGE (cd1:Cognitive_Distortion {type: 'Emotional reasoning'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);
MERGE (cd2:Cognitive_Distortion {type: 'Personalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);
MERGE (es:Erikson_Stage {name: 'Intimacy vs isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {name: 'Anxious preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (dm:Defense_Mechanism {name: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm);
MERGE (sch1:Schema {name: 'Abandonment'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch1);
MERGE (sch2:Schema {name: 'Social isolation alienation'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch2);
MERGE (bf:Big_Five {profile: 'qa_pair_021'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.6, extraversion: 0.5, agreeableness: 0.7, neuroticism: 0.7, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:41:51
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_022'});
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e_sadness:Emotion {name: 'Sadness'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.7, arousal: 0.5, confidence: 0.9}]->(e_sadness);
MERGE (e_frustration:Emotion {name: 'Frustration'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.6, arousal: 0.6, confidence: 0.8}]->(e_frustration);
MERGE (e_contentment:Emotion {name: 'Contentment'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.5, arousal: 0.3, confidence: 0.7}]->(e_contentment);
MERGE (e_melancholy:Emotion {name: 'Melancholy'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.4, confidence: 0.8}]->(e_melancholy);
MERGE (cd_overgeneralization:Cognitive_Distortion {type: 'Overgeneralization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd_overgeneralization);
MERGE (cd_personalization:Cognitive_Distortion {type: 'Personalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd_personalization);
MERGE (cd_catastrophizing:Cognitive_Distortion {type: 'Catastrophizing'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd_catastrophizing);
MERGE (es_intimacy:Erikson_Stage {name: 'Intimacy vs isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es_intimacy);
MERGE (as_anxious:Attachment_Style {name: 'Anxious preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as_anxious);
MERGE (dm_rationalization:Defense_Mechanism {name: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm_rationalization);
MERGE (sch_abandonment:Schema {name: 'Abandonment'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch_abandonment);
MERGE (sch_defectiveness:Schema {name: 'Defectiveness shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch_defectiveness);
MERGE (sch_isolation:Schema {name: 'Social isolation alienation'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch_isolation);
MERGE (bf_client:Big_Five {profile: 'client_profile'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.7, extraversion: 0.4, agreeableness: 0.6, neuroticism: 0.8, confidence: 0.7}]->(bf_client);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:42:20
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_023'});
MERGE (s)-[:INCLUDES]->(qa);

MERGE (e1:Emotion {name: 'Negative affect'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.6, arousal: 0.3, confidence: 0.8}]->(e1);

MERGE (e2:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.4, confidence: 0.7}]->(e2);

MERGE (e3:Emotion {name: 'Curiosity/novelty'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.4, arousal: 0.5, confidence: 0.6}]->(e3);

MERGE (cd1:Cognitive_Distortion {type: 'Overgeneralization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);

MERGE (cd2:Cognitive_Distortion {type: 'Mind reading'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);

MERGE (cd3:Cognitive_Distortion {type: 'Emotional reasoning'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd3);

MERGE (cd4:Cognitive_Distortion {type: 'Personalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd4);

MERGE (es:Erikson_Stage {name: 'Intimacy vs isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);

MERGE (as:Attachment_Style {name: 'Fearful-avoidant'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);

MERGE (dm1:Defense_Mechanism {name: 'Denial'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm1);

MERGE (dm2:Defense_Mechanism {name: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm2);

MERGE (dm3:Defense_Mechanism {name: 'Projection'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.5}]->(dm3);

MERGE (sch1:Schema {name: 'Abandonment'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch1);

MERGE (sch2:Schema {name: 'Defectiveness shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch2);

MERGE (sch3:Schema {name: 'Emotional deprivation'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch3);

MERGE (bf:Big_Five {profile: 'qa_pair_023'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.4, extraversion: 0.5, agreeableness: 0.3, neuroticism: 0.8, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:42:48
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_024'});
MERGE (s)-[:INCLUDES]->(qa);

MERGE (e_boredom:Emotion {name: 'Boredom'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.3, arousal: 0.1, confidence: 0.8}]->(e_boredom);

MERGE (e_amusement:Emotion {name: 'Amusement'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.4, arousal: 0.2, confidence: 0.7}]->(e_amusement);

MERGE (e_contentment:Emotion {name: 'Contentment'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.3, arousal: 0.1, confidence: 0.6}]->(e_contentment);

MERGE (cd:Cognitive_Distortion {type: 'Emotional reasoning'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd);

MERGE (es:Erikson_Stage {name: 'Intimacy vs isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);

MERGE (as:Attachment_Style {name: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);

MERGE (dm:Defense_Mechanism {name: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm);

MERGE (sch:Schema {name: 'Social isolation alienation'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch);

MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.6, conscientiousness: 0.5, extraversion: 0.4, agreeableness: 0.7, neuroticism: 0.3, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:43:35
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_025'});
MERGE (s)-[:INCLUDES]->(qa);

MERGE (e_sad:Emotion {name: 'Sadness'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.7, arousal: 0.5, confidence: 0.9}]->(e_sad);

MERGE (e_lon:Emotion {name: 'Loneliness'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.6, arousal: 0.4, confidence: 0.8}]->(e_lon);

MERGE (e_frust:Emotion {name: 'Frustration'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.6, confidence: 0.7}]->(e_frust);

MERGE (e_nost:Emotion {name: 'Nostalgia'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.4, arousal: 0.3, confidence: 0.6}]->(e_nost);

MERGE (cd_over:Cognitive_Distortion {type: 'Overgeneralization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd_over);

MERGE (cd_person:Cognitive_Distortion {type: 'Personalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd_person);

MERGE (cd_label:Cognitive_Distortion {type: 'Labeling'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd_label);

MERGE (es_intimacy:Erikson_Stage {name: 'Intimacy vs isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.9}]->(es_intimacy);

MERGE (as_anxious:Attachment_Style {name: 'Anxious preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as_anxious);

MERGE (dm_rational:Defense_Mechanism {name: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm_rational);

MERGE (dm_denial:Defense_Mechanism {name: 'Denial'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm_denial);

MERGE (sch_abandon:Schema {name: 'Abandonment'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch_abandon);

MERGE (sch_isolation:Schema {name: 'Social isolation alienation'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch_isolation);

MERGE (sch_self:Schema {name: 'Self-sacrifice'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch_self);

MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.6, conscientiousness: 0.8, extraversion: 0.3, agreeableness: 0.5, neuroticism: 0.8, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:44:04
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_026'});
MERGE (s)-[:INCLUDES]->(qa);

MERGE (e1:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.7, arousal: 0.6, confidence: 0.8}]->(e1);

MERGE (e2:Emotion {name: 'Resignation'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.4, confidence: 0.7}]->(e2);

MERGE (e3:Emotion {name: 'Self-justification'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.0, arousal: 0.3, confidence: 0.6}]->(e3);

MERGE (cd1:Cognitive_Distortion {type: 'All_or_nothing_thinking'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd1);

MERGE (cd2:Cognitive_Distortion {type: 'Overgeneralization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd2);

MERGE (cd3:Cognitive_Distortion {type: 'Mind_reading'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd3);

MERGE (cd4:Cognitive_Distortion {type: 'Personalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd4);

MERGE (es:Erikson_Stage {name: 'Intimacy_vs_isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);

MERGE (as:Attachment_Style {name: 'Anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);

MERGE (dm1:Defense_Mechanism {name: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.8}]->(dm1);

MERGE (dm2:Defense_Mechanism {name: 'Denial'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm2);

MERGE (dm3:Defense_Mechanism {name: 'Projection'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.5}]->(dm3);

MERGE (sch1:Schema {name: 'Defectiveness_shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch1);

MERGE (sch2:Schema {name: 'Self_sacrifice'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch2);

MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.6, conscientiousness: 0.7, extraversion: 0.3, agreeableness: 0.5, neuroticism: 0.8, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:44:30
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_027'});
MERGE (s)-[:INCLUDES]->(qa);

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

MERGE (es:Erikson_Stage {name: 'Industry vs Inferiority'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);

MERGE (as:Attachment_Style {name: 'Anxious preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);

MERGE (dm1:Defense_Mechanism {name: 'Humor'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.8}]->(dm1);

MERGE (dm2:Defense_Mechanism {name: 'Avoidance'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm2);

MERGE (sch:Schema {name: 'Defectiveness shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.8}]->(sch);

MERGE (bf:Big_Five {profile: 'qa_pair_027'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.8, extraversion: 0.5, agreeableness: 0.6, neuroticism: 0.5, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:45:01
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_028'});
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Enthusiasm'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.9, arousal: 0.7, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Calm'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.8, arousal: 0.2, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Sociability'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.6, confidence: 0.8}]->(e3);
MERGE (es:Erikson_Stage {name: 'Identity_vs_role_confusion'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.7}]->(es);
MERGE (as:Attachment_Style {name: 'Anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (dm:Defense_Mechanism {name: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm);
MERGE (sch:Schema {name: 'Approval_seeking'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch);
MERGE (bf:Big_Five {profile: 'qa_pair_028'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 1.0, conscientiousness: 1.0, extraversion: 0.57, agreeableness: 1.0, neuroticism: 0.14, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:45:46
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_029'});
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Contentment'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.4, confidence: 0.8}]->(e1);
MERGE (e2:Emotion {name: 'Determination'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.6, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Guilt'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.5, confidence: 0.7}]->(e3);
MERGE (e4:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.5, confidence: 0.7}]->(e4);
MERGE (cd:Cognitive_Distortion {type: 'Rationalization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.8}]->(cd);
MERGE (es:Erikson_Stage {name: 'intimacy_vs_isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {name: 'anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);
MERGE (dm:Defense_Mechanism {name: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.8}]->(dm);
MERGE (sch:Schema {name: 'Self_sacrifice'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch);
MERGE (bf:Big_Five {profile: 'Self_sacrifice'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.8, extraversion: 0.5, agreeableness: 0.8, neuroticism: 0.5, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:46:27
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_030'});
MERGE (s)-[:INCLUDES]->(qa);

MERGE (e1:Emotion {name: 'Anger'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.7, arousal: 0.8, confidence: 0.8}]->(e1);

MERGE (e2:Emotion {name: 'Frustration'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.6, arousal: 0.7, confidence: 0.7}]->(e2);

MERGE (e3:Emotion {name: 'Sadness'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.8, arousal: 0.3, confidence: 0.8}]->(e3);

MERGE (e4:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.6, confidence: 0.7}]->(e4);

MERGE (cd1:Cognitive_Distortion {type: 'Jumping to conclusions'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.7}]->(cd1);

MERGE (cd2:Cognitive_Distortion {type: 'Overgeneralization'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd2);

MERGE (es:Erikson_Stage {name: 'Intimacy vs isolation'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.7}]->(es);

MERGE (as:Attachment_Style {name: 'Anxious preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);

MERGE (dm1:Defense_Mechanism {name: 'Suppression'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm1);

MERGE (dm2:Defense_Mechanism {name: 'Avoidance'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm2);

MERGE (sch1:Schema {name: 'Emotional inhibition'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch1);

MERGE (sch2:Schema {name: 'Vulnerability to harm'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch2);

MERGE (bf:Big_Five {profile: 'qa_pair_030'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.7, extraversion: 0.4, agreeableness: 0.6, neuroticism: 0.8, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:46:50
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_031'});
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Contentment'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.4, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Motivation'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.8, arousal: 0.5, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Calm'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.3, confidence: 0.8}]->(e3);
MERGE (e4:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.6, confidence: 0.7}]->(e4);
MERGE (es:Erikson_Stage {name: 'Autonomy vs shame/doubt'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {name: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (bf:Big_Five {profile: 'qa_pair_031'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.6, extraversion: 0.5, agreeableness: 0.7, neuroticism: 0.3, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:47:11
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_032'});
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Contentment'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.4, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Motivation'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.8, arousal: 0.5, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Calm'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.3, confidence: 0.8}]->(e3);
MERGE (e4:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.6, confidence: 0.7}]->(e4);
MERGE (es:Erikson_Stage {name: 'Autonomy_vs_shame_doubt'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {name: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (bf:Big_Five {profile: 'qa_pair_032'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.6, extraversion: 0.5, agreeableness: 0.7, neuroticism: 0.3, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:54:48
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_033'});
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Contentment'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.7, arousal: 0.4, confidence: 0.9}]->(e1);
MERGE (e2:Emotion {name: 'Motivation'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.8, arousal: 0.5, confidence: 0.8}]->(e2);
MERGE (e3:Emotion {name: 'Calm'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.6, arousal: 0.3, confidence: 0.8}]->(e3);
MERGE (e4:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.6, confidence: 0.7}]->(e4);
MERGE (es:Erikson_Stage {name: 'Autonomy_vs_shame/doubt'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {name: 'Secure'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (bf:Big_Five {profile: 'qa_pair_033'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.6, extraversion: 0.5, agreeableness: 0.7, neuroticism: 0.3, confidence: 0.8}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-15 23:57:28
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_034'});
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e:Emotion {name: 'negative'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.6, confidence: 0.8}]->(e);
MERGE (cd:Cognitive_Distortion {type: 'Magnification'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd);
MERGE (es:Erikson_Stage {name: 'Industry_vs_inferiority'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.5}]->(es);
MERGE (as:Attachment_Style {name: 'Anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.5, conscientiousness: 0.7, extraversion: 0.4, agreeableness: 0.6, neuroticism: 0.7, confidence: 0.7}]->(bf);
MERGE (sch:Schema {name: 'Defectiveness_shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch);

// ============================================================================


// ============================================================================
// CYPHER ENTRY - 2025-09-16 00:03:42
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_035'});
MERGE (s)-[:INCLUDES]->(qa);
MERGE (e1:Emotion {name: 'Anxiety'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.4, arousal: 0.7, confidence: 0.8}]->(e1);
MERGE (e2:Emotion {name: 'Sadness'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.6, arousal: 0.5, confidence: 0.7}]->(e2);
MERGE (e3:Emotion {name: 'Relief'});
CREATE (qa)-[:REVEALS_EMOTION {valence: 0.5, arousal: 0.3, confidence: 0.7}]->(e3);
MERGE (e4:Emotion {name: 'Negative Valence'});
CREATE (qa)-[:REVEALS_EMOTION {valence: -0.5, arousal: 0.6, confidence: 0.8}]->(e4);
MERGE (cd:Cognitive_Distortion {type: 'Magnification'});
CREATE (qa)-[:EXHIBITS_DISTORTION {confidence: 0.6}]->(cd);
MERGE (es:Erikson_Stage {name: 'Industry_vs_inferiority'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.5}]->(es);
MERGE (as:Attachment_Style {name: 'Anxious_preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.7}]->(as);
MERGE (sch:Schema {name: 'Defectiveness_shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.5, conscientiousness: 0.7, extraversion: 0.4, agreeableness: 0.6, neuroticism: 0.7, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 00:04:18
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_036'});
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
MERGE (es:Erikson_Stage {name: 'Identity vs role confusion'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.7}]->(es);
MERGE (as:Attachment_Style {name: 'Anxious preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.6}]->(as);
MERGE (dm:Defense_Mechanism {name: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.6}]->(dm);
MERGE (sch1:Schema {name: 'Defectiveness shame'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.7}]->(sch1);
MERGE (sch2:Schema {name: 'Failure'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch2);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.6, conscientiousness: 0.4, extraversion: 0.5, agreeableness: 0.5, neuroticism: 0.7, confidence: 0.7}]->(bf);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 00:04:59
// ============================================================================

MATCH (s:Session {session_id: 'session_001'});
CREATE (qa:QA_Pair {id: 'qa_pair_037'});
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
MERGE (es:Erikson_Stage {name: 'Industry vs Inferiority'});
CREATE (qa)-[:EXHIBITS_STAGE {confidence: 0.8}]->(es);
MERGE (as:Attachment_Style {name: 'Anxious preoccupied'});
CREATE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: 0.8}]->(as);
MERGE (dm:Defense_Mechanism {name: 'Rationalization'});
CREATE (qa)-[:USES_DEFENSE_MECHANISM {confidence: 0.7}]->(dm);
MERGE (sch:Schema {name: 'Emotional deprivation'});
CREATE (qa)-[:REVEALS_SCHEMA {confidence: 0.6}]->(sch);
MERGE (bf:Big_Five {profile: 'individual'});
CREATE (qa)-[:SHOWS_BIG_FIVE {openness: 0.8, conscientiousness: 0.9, extraversion: 0.5, agreeableness: 0.6, neuroticism: 0.8, confidence: 0.8}]->(bf);
