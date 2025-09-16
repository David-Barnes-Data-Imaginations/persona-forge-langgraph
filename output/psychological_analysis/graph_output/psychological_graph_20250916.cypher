
// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:45:57
// ============================================================================

MERGE (c:Client {id: 'client_001'})
MERGE (s:Session {session_id: 'session_001'})
MERGE (c)-[:PARTICIPATED_IN]->(s);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:46:09
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_001',
    emotions: [
      {name:'Empathy', valence:0.2, arousal:0.3, confidence:0.8},
      {name:'Anger visualization', valence:0.5, arousal:0.7, confidence:0.7},
      {name:'Sadness when others sad', valence:-0.4, arousal:0.4, confidence:0.7}
    ],
    distortions: [
      {type:'Rationalization', confidence:0.7}
    ],
    stages: [
      {name:'Identity_vs_role_confusion', confidence:0.7}
    ],
    attachments: [
      {name:'Anxious_preoccupied', confidence:0.7}
    ],
    defenses: [
      {name:'Denial', confidence:0.6},
      {name:'Intellectualization', confidence:0.6}
    ],
    schemas: [
      {name:'Emotional_deprivation', confidence:0.7}
    ],
    bigfive: {
      profile:'individual',
      openness:0.8,
      conscientiousness:0.6,
      extraversion:0.4,
      agreeableness:0.5,
      neuroticism:0.5,
      confidence:0.7
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness, conscientiousness: bf.conscientiousness, extraversion: bf.extraversion,
    agreeableness: bf.agreeableness, neuroticism: bf.neuroticism, confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:46:58
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_002', emotions: [ {name:'Calm', valence:0.2, arousal:0.1, confidence:0.9},
    {name:'Detached', valence:0.1, arousal:0.05, confidence:0.8},
    {name:'Self‑assertive', valence:0.3, arousal:0.15, confidence:0.7},
    {name:'Altruistic', valence:0.25, arousal:0.1, confidence:0.7}
  ], distortions: [
    {type:'Minimization', confidence:0.7}, {type:'All or nothing thinking', confidence:0.6}
  ], stages: [ {name:'Intimacy vs isolation', confidence:0.7}
  ],
    attachments: [
             {name:'Dismissive avoidant', confidence:0.8}
           ],
    defenses: [
             {name:'Denial', confidence:0.7},
             {name:'Rationalization', confidence:0.6}
           ],
    schemas: [
             {name:'Self‑sacrifice', confidence:0.8}
           ],
    bigfive: { profile:'individual', openness:0.8, conscientiousness:0.8, extraversion:0.3, agreeableness:0.7, neuroticism:0.2, confidence:0.7 } }
]AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a) )
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m) )
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness, conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:47:25
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_003',
    emotions: [
      {name:'Calm Detachment', valence:0.6, arousal:0.2, confidence:0.9},
      {name:'Emotional Exhaustion', valence:-0.7, arousal:0.8, confidence:0.8},
      {name:'Neutral Detachment', valence:0.0, arousal:0.1, confidence:0.8},
      {name:'Anxiety in Social Context', valence:-0.4, arousal:0.5, confidence:0.7}
    ],
    distortions: [
      {type:'Labeling', confidence:0.8},
      {type:'Personalization', confidence:0.7}
    ],
    stages: [
      {name:'Generativity vs stagnation', confidence:0.8}
    ],
    attachments: [
      {name:'Anxious preoccupied', confidence:0.7}
    ],
    defenses: [
      {name:'Suppression', confidence:0.8}
    ],
    schemas: [
      {name:'Defectiveness shame', confidence:0.8}
    ],
    bigfive: {
      profile:'individual',
      openness:0.8,
      conscientiousness:0.7,
      extraversion:0.4,
      agreeableness:0.6,
      neuroticism:0.7,
      confidence:0.8
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:47:59
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  { qa_id: 'qa_pair_004', emotions: [
    {name:'Enthusiasm', valence:0.8, arousal:0.7, confidence:0.9},
    {name:'Anxiety', valence:-0.2, arousal:0.3, confidence:0.6}
  ],
    distortions: [],
    stages: [
             {name:'Initiative_vs_guilt', confidence:0.7}
           ],
    attachments: [
             {name:'Secure', confidence:0.8}
           ], defenses: [],
    schemas: [],
    bigfive: {
             profile:'individual',
             openness:0.9,
             conscientiousness:0.6,
             extraversion:0.7,
             agreeableness:0.6,
             neuroticism:0.3,
             confidence:0.8
           }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {openness: bf.openness, conscientiousness: bf.conscientiousness, extraversion: bf.extraversion, agreeableness: bf.agreeableness, neuroticism: bf.neuroticism, confidence: bf.confidence}]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:48:31
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  { qa_id: 'qa_pair_005', emotions: [
    {name:'Enthusiasm', valence:0.8, arousal:0.7, confidence:0.9},
    {name:'Anxiety', valence:-0.2, arousal:0.3, confidence:0.6} ],
    distortions: [],
    stages: [{name:'Initiative_vs_guilt', confidence:0.7}],
    attachments: [{name:'Secure', confidence:0.8}],
    defenses: [],
    schemas: [],
    bigfive: {
             profile:'individual',
             openness:0.9,
             conscientiousness:0.6,
             extraversion:0.7,
             agreeableness:0.6,
             neuroticism:0.3,
             confidence:0.8} }
]AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name}
  )
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2) )
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence}]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:48:48
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_006',
    emotions: [
      {name:'Empathy', valence:0.7, arousal:0.4, confidence:0.9},
      {name:'Fulfillment', valence:0.8, arousal:0.3, confidence:0.8},
      {name:'Amusement', valence:0.6, arousal:0.2, confidence:0.7}
    ],
    distortions: [],
    stages: [{name:'Intimacy_vs_isolation', confidence:0.8}],
    attachments: [{name:'Secure', confidence:0.8}],
    defenses: [],
    schemas: [],
    bigfive: {profile:'individual', openness:0.8, conscientiousness:0.6, extraversion:0.5, agreeableness:0.8, neuroticism:0.3, confidence:0.8}
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness, conscientiousness: bf.conscientiousness, extraversion: bf.extraversion,
    agreeableness: bf.agreeableness, neuroticism: bf.neuroticism, confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:49:07
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_007',
    emotions: [
      {name:'Amusement', valence:0.6, arousal:0.4, confidence:0.8},
      {name:'Self‑deprecation', valence:-0.5, arousal:0.5, confidence:0.7},
      {name:'Pride', valence:0.5, arousal:0.3, confidence:0.7},
      {name:'Anxiety', valence:-0.4, arousal:0.6, confidence:0.6}
    ],
    distortions: [
      {type:'Overgeneralization', confidence:0.8},
      {type:'Emotional reasoning', confidence:0.7}
    ],
    stages: [
      {name:'Identity vs role confusion', confidence:0.8}
    ],
    attachments: [
      {name:'Anxious preoccupied', confidence:0.7}
    ],
    defenses: [
      {name:'Rationalization', confidence:0.7}
    ],
    schemas: [
      {name:'Defectiveness shame', confidence:0.8}
    ],
    bigfive: {
      profile:'individual',
      openness:0.9,
      conscientiousness:0.5,
      extraversion:0.6,
      agreeableness:0.4,
      neuroticism:0.7,
      confidence:0.7
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness, conscientiousness: bf.conscientiousness, extraversion: bf.extraversion,
    agreeableness: bf.agreeableness, neuroticism: bf.neuroticism, confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:49:49
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_008',
    emotions: [
      {name:'Curiosity', valence:0.6, arousal:0.7, confidence:0.9},
      {name:'Pride', valence:0.5, arousal:0.5, confidence:0.8},
      {name:'Anxiety', valence:-0.3, arousal:0.6, confidence:0.7}
    ],
    distortions: [
      {type:'Labeling', confidence:0.8},
      {type:'Should statements', confidence:0.7}
    ],
    stages: [
      {name:'Identity vs role confusion', confidence:0.8}
    ],
    attachments: [
      {name:'Secure', confidence:0.8}
    ],
    defenses: [
      {name:'Rationalization', confidence:0.7}
    ],
    schemas: [
      {name:'Approval seeking', confidence:0.7}
    ],
    bigfive: {
      profile:'individual',
      openness:0.9,
      conscientiousness:0.8,
      extraversion:0.5,
      agreeableness:0.8,
      neuroticism:0.4,
      confidence:0.8
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness, conscientiousness: bf.conscientiousness, extraversion: bf.extraversion,
    agreeableness: bf.agreeableness, neuroticism: bf.neuroticism, confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:50:23
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_009',
    emotions: [
      {name:'Pride', valence:0.7, arousal:0.4, confidence:0.8},
      {name:'Humor', valence:0.6, arousal:0.3, confidence:0.7},
      {name:'Self‑deprecation', valence:-0.4, arousal:0.2, confidence:0.6},
      {name:'Protective motivation', valence:0.5, arousal:0.3, confidence:0.7}
    ],
    distortions: [
      {type:'Personalization', confidence:0.7},
      {type:'Should statements', confidence:0.6}
    ],
    stages: [
      {name:'generativity_vs_stagnation', confidence:0.8}
    ],
    attachments: [
      {name:'Secure', confidence:0.8}
    ],
    defenses: [
      {name:'Humor', confidence:0.7}
    ],
    schemas: [
      {name:'Self‑sacrifice', confidence:0.7},
      {name:'Approval seeking', confidence:0.6}
    ],
    bigfive: {
      profile:'individual',
      openness:0.8,
      conscientiousness:0.7,
      extraversion:0.5,
      agreeableness:0.7,
      neuroticism:0.4,
      confidence:0.7
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE
  {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:51:21
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_011',
    emotions: [
      {name:'Anxiety', valence:-0.8, arousal:0.9, confidence:0.9},
      {name:'Relief', valence:0.6, arousal:0.4, confidence:0.7},
      {name:'Frustration', valence:-0.5, arousal:0.6, confidence:0.6},
      {name:'Hope', valence:0.4, arousal:0.3, confidence:0.5}
    ],
    distortions: [
      {type:'Personalization', confidence:0.8},
      {type:'Emotional reasoning', confidence:0.7},
      {type:'Overgeneralization', confidence:0.6}
    ],
    stages: [
      {name:'Identity vs role confusion', confidence:0.7}
    ],
    attachments: [
      {name:'Anxious preoccupied', confidence:0.8}
    ],
    defenses: [
      {name:'Rationalization', confidence:0.8}
    ],
    schemas: [
      {name:'Self‑sacrifice', confidence:0.7}
    ],
    bigfive: {
      profile:'individual',
      openness:0.8,
      conscientiousness:0.7,
      extraversion:0.4,
      agreeableness:0.7,
      neuroticism:0.9,
      confidence:0.8
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:51:52
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_012',
    emotions: [
      {name:'Enthusiasm', valence:0.8, arousal:0.5, confidence:0.9},
      {name:'Humor', valence:0.6, arousal:0.3, confidence:0.7},
      {name:'Calm', valence:0.5, arousal:0.2, confidence:0.8}
    ],
    distortions: [
      {type:'Minimization', confidence:0.7},
      {type:'Rationalization', confidence:0.6}
    ],
    stages: [
      {name:'Generativity_vs_stagnation', confidence:0.8}
    ],
    attachments: [
      {name:'Secure', confidence:0.8}
    ],
    defenses: [
      {name:'Humor', confidence:0.8},
      {name:'Rationalization', confidence:0.7},
      {name:'Intellectualization', confidence:0.6}
    ],
    schemas: [
      {name:'Approval_seeking', confidence:0.7}
    ],
    bigfive: {
      profile:'individual',
      openness:0.8,
      conscientiousness:0.9,
      extraversion:0.6,
      agreeableness:0.8,
      neuroticism:0.3,
      confidence:0.8
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE
  {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:52:11
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_013',
    emotions: [
      {name:'Contentment', valence:0.7, arousal:0.4, confidence:0.9},
      {name:'Anxiety', valence:-0.5, arousal:0.6, confidence:0.8},
      {name:'Determination', valence:0.6, arousal:0.5, confidence:0.8},
      {name:'Self‑criticism', valence:-0.4, arousal:0.5, confidence:0.7}
    ],
    distortions: [
      {type:'All or nothing thinking', confidence:0.7},
      {type:'Catastrophizing', confidence:0.6},
      {type:'Emotional reasoning', confidence:0.6}
    ],
    stages: [
      {name:'Generativity vs stagnation', confidence:0.8}
    ],
    attachments: [
      {name:'Anxious preoccupied', confidence:0.7}
    ],
    defenses: [
      {name:'Intellectualization', confidence:0.8},
      {name:'Suppression', confidence:0.6}
    ],
    schemas: [
      {name:'Vulnerability to harm', confidence:0.7},
      {name:'Emotional inhibition', confidence:0.6}
    ],
    bigfive: {
      profile:'individual',
      openness:0.8,
      conscientiousness:0.8,
      extraversion:0.4,
      agreeableness:0.7,
      neuroticism:0.6,
      confidence:0.7
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:52:37
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_014',
    emotions: [
      {name:'Enthusiasm', valence:0.8, arousal:0.6, confidence:0.9}
    ],
    distortions: [],
    stages: [{name:'Identity_vs_role_confusion', confidence:0.7}],
    attachments: [{name:'Secure', confidence:0.8}],
    defenses: [],
    schemas: [],
    bigfive: {profile:'individual', openness:0.9,
              conscientiousness:0.8,
              extraversion:0.5,
              agreeableness:0.7,
              neuroticism:0.3,
              confidence:0.8}
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:52:55
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_015',
    emotions: [
      {name:'Optimism', valence:0.7, arousal:0.4, confidence:0.9}
    ],
    distortions: [
      {type:'Overgeneralization', confidence:0.8},
      {type:'Minimization', confidence:0.7}
    ],
    stages: [
      {name:'Industry_vs_inferiority', confidence:0.8}
    ],
    attachments: [
      {name:'Secure', confidence:0.7}
    ],
    defenses: [
      {name:'Rationalization', confidence:0.7},
      {name:'Intellectualization', confidence:0.6}
    ],
    schemas: [],
    bigfive: {
      profile:'individual',
      openness:0.9,
      conscientiousness:0.7,
      extraversion:0.4,
      agreeableness:0.5,
      neuroticism:0.3,
      confidence:0.8
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness, conscientiousness: bf.conscientiousness, extraversion: bf.extraversion,
    agreeableness: bf.agreeableness, neuroticism: bf.neuroticism, confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:53:14
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_016',
    emotions: [
      {name:'Anger', valence:-0.8, arousal:0.9, confidence:0.9},
      {name:'Frustration', valence:-0.7, arousal:0.8, confidence:0.8},
      {name:'Anxiety', valence:-0.6, arousal:0.8, confidence:0.8},
      {name:'Distrust', valence:-0.6, arousal:0.7, confidence:0.7}
    ],
    distortions: [
      {type:'Catastrophizing', confidence:0.8},
      {type:'Overgeneralization', confidence:0.7},
      {type:'Personalization', confidence:0.7},
      {type:'Mind reading', confidence:0.6},
      {type:'Emotional reasoning', confidence:0.6}
    ],
    stages: [
      {name:'Intimacy_vs_isolation', confidence:0.8}
    ],
    attachments: [
      {name:'Anxious_preoccupied', confidence:0.8}
    ],
    defenses: [
      {name:'Denial', confidence:0.7},
      {name:'Rationalization', confidence:0.7}
    ],
    schemas: [
      {name:'Mistrust_abuse', confidence:0.8},
      {name:'Emotional_inhibition', confidence:0.6}
    ],
    bigfive: {
      profile:'individual',
      openness:0.9,
      conscientiousness:0.6,
      extraversion:0.7,
      agreeableness:0.4,
      neuroticism:0.8,
      confidence:0.8
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness, conscientiousness: bf.conscientiousness, extraversion: bf.extraversion,
    agreeableness: bf.agreeableness, neuroticism: bf.neuroticism, confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:53:43
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_017',
    emotions: [
      {name:'Anxiety', valence:-0.8, arousal:0.7, confidence:0.9},
      {name:'Hope', valence:0.6, arousal:0.4, confidence:0.8},
      {name:'Sadness', valence:-0.6, arousal:0.3, confidence:0.7}
    ],
    distortions: [
      {type:'Catastrophizing', confidence:0.8},
      {type:'All_or_nothing_thinking', confidence:0.7},
      {type:'Emotional_reasoning', confidence:0.6}
    ],
    stages: [
      {name:'Identity_vs_role_confusion', confidence:0.8}
    ],
    attachments: [
      {name:'Anxious_preoccupied', confidence:0.8}
    ],
    defenses: [
      {name:'Intellectualization', confidence:0.7}
    ],
    schemas: [
      {name:'Defectiveness_shame', confidence:0.8},
      {name:'Failure', confidence:0.6}
    ],
    bigfive: {profile:'individual', openness:0.9, conscientiousness:0.5, extraversion:0.3, agreeableness:0.6, neuroticism:0.9, confidence:0.8}
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness, conscientiousness: bf.conscientiousness, extraversion: bf.extraversion,
    agreeableness: bf.agreeableness, neuroticism: bf.neuroticism, confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:54:14
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_018',
    emotions: [
      {name:'Calm', valence:0.7, arousal:-0.4, confidence:0.9},
      {name:'Empathy', valence:0.6, arousal:-0.2, confidence:0.8},
      {name:'Exhaustion', valence:-0.4, arousal:0.3, confidence:0.7},
      {name:'Misunderstood', valence:-0.3, arousal:0.2, confidence:0.7}
    ],
    distortions: [
      {type:'Mind reading', confidence:0.8},
      {type:'Overgeneralization', confidence:0.7}
    ],
    stages: [
      {name:'Integrity vs despair', confidence:0.8}
    ],
    attachments: [
      {name:'Anxious preoccupied', confidence:0.8}
    ],
    defenses: [
      {name:'Rationalization', confidence:0.8},
      {name:'Intellectualization', confidence:0.7}
    ],
    schemas: [
      {name:'Self-sacrifice', confidence:0.8},
      {name:'Emotional inhibition', confidence:0.7}
    ],
    bigfive: {profile:'individual', openness:0.8, conscientiousness:0.7, extraversion:0.3, agreeableness:0.8, neuroticism:0.5, confidence:0.8}
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:54:43
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_019',
    emotions: [
      {name:'Empathy', valence:0.6, arousal:0.4, confidence:0.9},
      {name:'Guilt', valence:-0.7, arousal:0.6, confidence:0.8},
      {name:'Sadness', valence:-0.6, arousal:0.5, confidence:0.7},
      {name:'Relief', valence:0.5, arousal:0.3, confidence:0.8}
    ],
    distortions: [
      {type:'Should statements', confidence:0.8},
      {type:'Personalization', confidence:0.7},
      {type:'Emotional reasoning', confidence:0.6},
      {type:'Catastrophizing', confidence:0.5}
    ],
    stages: [
      {name:'Intimacy vs isolation', confidence:0.8}
    ],
    attachments: [
      {name:'Anxious preoccupied', confidence:0.8}
    ],
    defenses: [
      {name:'Rationalization', confidence:0.7},
      {name:'Denial', confidence:0.6},
      {name:'Suppression', confidence:0.6}
    ],
    schemas: [
      {name:'Self-sacrifice', confidence:0.8},
      {name:'Defectiveness shame', confidence:0.7},
      {name:'Approval seeking', confidence:0.6}
    ],
    bigfive: {
      profile:'individual',
      openness:0.8,
      conscientiousness:0.8,
      extraversion:0.4,
      agreeableness:0.7,
      neuroticism:0.8,
      confidence:0.7
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:55:18
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_020',
    emotions: [
      {name:'Gratitude', valence:0.7, arousal:0.5, confidence:0.9},
      {name:'Sadness', valence:-0.6, arousal:0.6, confidence:0.8},
      {name:'Awe/Relief', valence:0.6, arousal:0.4, confidence:0.8},
      {name:'Anxiety', valence:-0.4, arousal:0.5, confidence:0.7}
    ],
    distortions: [
      {type:'Personalization', confidence:0.8},
      {type:'Emotional Reasoning', confidence:0.7}
    ],
    stages: [
      {name:'Identity_vs_Role_Confusion', confidence:0.8}
    ],
    attachments: [
      {name:'Anxious_Preoccupied', confidence:0.8}
    ],
    defenses: [
      {name:'Intellectualization', confidence:0.6}
    ],
    schemas: [
      {name:'Defectiveness/ Shame', confidence:0.8}
    ],
    bigfive: {
      profile:'individual',
      openness:0.8,
      conscientiousness:0.7,
      extraversion:0.5,
      agreeableness:0.8,
      neuroticism:0.7,
      confidence:0.8
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness, conscientiousness: bf.conscientiousness, extraversion: bf.extraversion,
    agreeableness: bf.agreeableness, neuroticism: bf.neuroticism, confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:55:48
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_021',
    emotions: [
      {name:'nostalgia', valence:0.7, arousal:0.5, confidence:0.8},
      {name:'gratitude', valence:0.6, arousal:0.4, confidence:0.7},
      {name:'sadness', valence:-0.5, arousal:0.6, confidence:0.8},
      {name:'loneliness', valence:-0.4, arousal:0.5, confidence:0.7}
    ],
    distortions: [
      {type:'emotional_reasoning', confidence:0.8},
      {type:'personalization', confidence:0.7}
    ],
    stages: [
      {name:'intimacy_vs_isolation', confidence:0.8}
    ],
    attachments: [
      {name:'anxious_preoccupied', confidence:0.8}
    ],
    defenses: [
      {name:'rationalization', confidence:0.7}
    ],
    schemas: [
      {name:'abandonment', confidence:0.7},
      {name:'social_isolation_alienation', confidence:0.8}
    ],
    bigfive: {
      profile:'individual',
      openness:0.8,
      conscientiousness:0.6,
      extraversion:0.5,
      agreeableness:0.7,
      neuroticism:0.7,
      confidence:0.7
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:56:20
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_022',
    emotions: [
      {name:'Sadness', valence:-0.7, arousal:0.5, confidence:0.9},
      {name:'Frustration', valence:-0.6, arousal:0.6, confidence:0.8},
      {name:'Contentment', valence:0.5, arousal:0.3, confidence:0.7},
      {name:'Melancholy', valence:-0.5, arousal:0.4, confidence:0.8}
    ],
    distortions: [
      {type:'Overgeneralization', confidence:0.8},
      {type:'Personalization', confidence:0.7},
      {type:'Catastrophizing', confidence:0.6}
    ],
    stages: [
      {name:'intimacy_vs_isolation', confidence:0.8}
    ],
    attachments: [
      {name:'anxious_preoccupied', confidence:0.8}
    ],
    defenses: [
      {name:'Rationalization', confidence:0.7}
    ],
    schemas: [
      {name:'Abandonment', confidence:0.8},
      {name:'Defectiveness_shame', confidence:0.7},
      {name:'Social_isolation_alienation', confidence:0.6}
    ],
    bigfive: {
      profile:'individual',
      openness:0.8,
      conscientiousness:0.7,
      extraversion:0.4,
      agreeableness:0.6,
      neuroticism:0.8,
      confidence:0.7
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:56:51
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_023',
    emotions: [
      {name:'Negative affect', valence:-0.6, arousal:0.3, confidence:0.8},
      {name:'Anxiety', valence:-0.5, arousal:0.4, confidence:0.7},
      {name:'Curiosity/novelty', valence:0.4, arousal:0.5, confidence:0.6}
    ],
    distortions: [
      {type:'Overgeneralization', confidence:0.8},
      {type:'Mind reading', confidence:0.7},
      {type:'Emotional reasoning', confidence:0.6},
      {type:'Personalization', confidence:0.6}
    ],
    stages: [
      {name:'Intimacy vs isolation', confidence:0.8}
    ],
    attachments: [
      {name:'Fearful-avoidant', confidence:0.7}
    ],
    defenses: [
      {name:'Denial', confidence:0.7},
      {name:'Rationalization', confidence:0.6},
      {name:'Projection', confidence:0.5}
    ],
    schemas: [
      {name:'Abandonment', confidence:0.8},
      {name:'Defectiveness shame', confidence:0.7},
      {name:'Emotional deprivation', confidence:0.6}
    ],
    bigfive: {
      profile:'individual',
      openness:0.8,
      conscientiousness:0.4,
      extraversion:0.5,
      agreeableness:0.3,
      neuroticism:0.8,
      confidence:0.7
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:57:30
// ============================================================================

MATCH (s:Session {session_id: 'session_001'}) WITH s, [ { qa_id: 'qa_pair_024', emotions: [ {name:'Boredom', valence:-0.3, arousal:0.1, confidence:0.8}, {name:'Amusement', valence:0.4, arousal:0.2, confidence:0.7}, {name:'Contentment', valence:0.3, arousal:0.1, confidence:0.6} ], distortions: [ {type:'Emotional reasoning', confidence:0.7} ], stages: [ {name:'Intimacy_vs_isolation', confidence:0.8} ], attachments: [ {name:'Secure', confidence:0.8} ], defenses: [ {name:'Rationalization', confidence:0.6} ], schemas: [ {name:'Social_isolation_alienation', confidence:0.6} ], bigfive: { profile:'individual', openness:0.6, conscientiousness:0.5, extraversion:0.4, agreeableness:0.7, neuroticism:0.3, confidence:0.7 } } ] AS rows UNWIND rows AS r MERGE (qa:QA_Pair {id: r.qa_id}) MERGE (s)-[:INCLUDES]->(qa) WITH qa, r FOREACH (emo IN coalesce(r.emotions, []) | MERGE (e:Emotion {name: emo.name}) MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e) ) FOREACH (cd IN coalesce(r.distortions, []) | MERGE (d:Cognitive_Distortion {type: cd.type}) MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d) ) FOREACH (st IN coalesce(r.stages, []) | MERGE (es:Erikson_Stage {name: st.name}) MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es) ) FOREACH (as IN coalesce(r.attachments, []) | MERGE (a:Attachment_Style {name: as.name}) MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a) ) FOREACH (dm IN coalesce(r.defenses, []) | MERGE (m:Defense_Mechanism {name: dm.name}) MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m) ) FOREACH (sch IN coalesce(r.schemas, []) | MERGE (s2:Schema {name: sch.name}) MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2) ) FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END | MERGE (b:Big_Five {profile: bf.profile}) MERGE (qa)-[:SHOWS_BIG_FIVE { openness: bf.openness, conscientiousness: bf.conscientiousness, extraversion: bf.extraversion, agreeableness: bf.agreeableness, neuroticism: bf.neuroticism, confidence: bf.confidence }]->(b) );

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:58:03
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_025',
    emotions: [
      {name:'Sadness', valence:-0.7, arousal:0.5, confidence:0.9},
      {name:'Loneliness', valence:-0.6, arousal:0.4, confidence:0.8},
      {name:'Frustration', valence:-0.5, arousal:0.6, confidence:0.7},
      {name:'Nostalgia', valence:0.4, arousal:0.3, confidence:0.6}
    ],
    distortions: [
      {type:'Overgeneralization', confidence:0.8},
      {type:'Personalization', confidence:0.7},
      {type:'Labeling', confidence:0.6}
    ],
    stages: [
      {name:'Intimacy_vs_isolation', confidence:0.9}
    ],
    attachments: [
      {name:'Anxious_preoccupied', confidence:0.8}
    ],
    defenses: [
      {name:'Rationalization', confidence:0.7},
      {name:'Denial', confidence:0.6}
    ],
    schemas: [
      {name:'Abandonment', confidence:0.8},
      {name:'Social_isolation_alienation', confidence:0.7},
      {name:'Self-sacrifice', confidence:0.6}
    ],
    bigfive: {
      profile:'individual',
      openness:0.6,
      conscientiousness:0.8,
      extraversion:0.3,
      agreeableness:0.5,
      neuroticism:0.8,
      confidence:0.7
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:58:36
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_026',
    emotions: [
      {name:'Anxiety', valence:-0.7, arousal:0.6, confidence:0.8},
      {name:'Resignation', valence:-0.5, arousal:0.4, confidence:0.7},
      {name:'Self‑justification', valence:0.0, arousal:0.3, confidence:0.6}
    ],
    distortions: [
      {type:'All or nothing thinking', confidence:0.8},
      {type:'Overgeneralization', confidence:0.7},
      {type:'Mind reading', confidence:0.6},
      {type:'Personalization', confidence:0.7}
    ],
    stages: [
      {name:'Intimacy vs isolation', confidence:0.8}
    ],
    attachments: [
      {name:'Anxious preoccupied', confidence:0.7}
    ],
    defenses: [
      {name:'Rationalization', confidence:0.8},
      {name:'Denial', confidence:0.6},
      {name:'Projection', confidence:0.5}
    ],
    schemas: [
      {name:'Defectiveness shame', confidence:0.8},
      {name:'Self‑sacrifice', confidence:0.6}
    ],
    bigfive: {
      profile:'individual',
      openness:0.6,
      conscientiousness:0.7,
      extraversion:0.3,
      agreeableness:0.5,
      neuroticism:0.8,
      confidence:0.7
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:59:10
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_027',
    emotions: [
      {name:'Contentment', valence:0.7, arousal:0.3, confidence:0.9},
      {name:'Humor', valence:0.6, arousal:0.4, confidence:0.8},
      {name:'Frustration', valence:-0.4, arousal:0.5, confidence:0.7},
      {name:'Self‑efficacy', valence:0.8, arousal:0.2, confidence:0.9}
    ],
    distortions: [
      {type:'Overgeneralization', confidence:0.8},
      {type:'Labeling', confidence:0.7}
    ],
    stages: [
      {name:'Industry vs Inferiority', confidence:0.8}
    ],
    attachments: [
      {name:'Anxious preoccupied', confidence:0.7}
    ],
    defenses: [
      {name:'Humor', confidence:0.8},
      {name:'Avoidance', confidence:0.7}
    ],
    schemas: [
      {name:'Defectiveness shame', confidence:0.8}
    ],
    bigfive: {
      profile:'individual',
      openness:0.8,
      conscientiousness:0.8,
      extraversion:0.5,
      agreeableness:0.6,
      neuroticism:0.5,
      confidence:0.8
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:59:34
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_028',
    emotions: [
      {name:'Enthusiasm', valence:0.9, arousal:0.7, confidence:0.9},
      {name:'Calm', valence:0.8, arousal:0.2, confidence:0.8},
      {name:'Sociability', valence:0.7, arousal:0.6, confidence:0.8}
    ],
    distortions: [],
    stages: [{name:'Identity_vs_role_confusion', confidence:0.7}],
    attachments: [{name:'Anxious_preoccupied', confidence:0.8}],
    defenses: [{name:'Rationalization', confidence:0.7}],
    schemas: [{name:'Approval_seeking', confidence:0.7}],
    bigfive: {profile:'individual', openness:1.0, conscientiousness:1.0, extraversion:0.57, agreeableness:1.0, neuroticism:0.14, confidence:0.7}
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 14:00:02
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_029',
    emotions: [
      {name:'contentment', valence:0.7, arousal:0.4, confidence:0.8},
      {name:'determination', valence:0.6, arousal:0.6, confidence:0.8},
      {name:'guilt', valence:-0.5, arousal:0.5, confidence:0.7},
      {name:'anxiety', valence:-0.4, arousal:0.5, confidence:0.7}
    ],
    distortions: [
      {type:'rationalization', confidence:0.8}
    ],
    stages: [
      {name:'intimacy_vs_isolation', confidence:0.8}
    ],
    attachments: [
      {name:'anxious_preoccupied', confidence:0.7}
    ],
    defenses: [
      {name:'rationalization', confidence:0.8}
    ],
    schemas: [
      {name:'self_sacrifice', confidence:0.7}
    ],
    bigfive: {profile:'individual', openness:0.8, conscientiousness:0.8, extraversion:0.5, agreeableness:0.8, neuroticism:0.5, confidence:0.7}
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 14:00:26
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_030',
    emotions: [
      {name:'Anger', valence:-0.7, arousal:0.8, confidence:0.8},
      {name:'Frustration', valence:-0.6, arousal:0.7, confidence:0.7},
      {name:'Sadness', valence:-0.8, arousal:0.3, confidence:0.8},
      {name:'Anxiety', valence:-0.5, arousal:0.6, confidence:0.7}
    ],
    distortions: [
      {type:'Jumping to conclusions', confidence:0.7},
      {type:'Overgeneralization', confidence:0.6}
    ],
    stages: [
      {name:'Intimacy vs isolation', confidence:0.7}
    ],
    attachments: [
      {name:'Anxious preoccupied', confidence:0.7}
    ],
    defenses: [
      {name:'Suppression', confidence:0.6},
      {name:'Avoidance', confidence:0.6}
    ],
    schemas: [
      {name:'Emotional inhibition', confidence:0.7},
      {name:'Vulnerability to harm', confidence:0.6}
    ],
    bigfive: {
      profile:'individual',
      openness:0.8,
      conscientiousness:0.7,
      extraversion:0.4,
      agreeableness:0.6,
      neuroticism:0.8,
      confidence:0.7
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 14:00:48
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_031',
    emotions: [
      {name:'Contentment', valence:0.7, arousal:0.4, confidence:0.9},
      {name:'Motivation', valence:0.8, arousal:0.5, confidence:0.8},
      {name:'Calm', valence:0.6, arousal:0.3, confidence:0.8},
      {name:'Anxiety', valence:-0.4, arousal:0.6, confidence:0.7}
    ],
    distortions: [],
    stages: [
      {name:'Autonomy_vs_shame/doubt', confidence:0.8}
    ],
    attachments: [
      {name:'Secure', confidence:0.8}
    ],
    defenses: [],
    schemas: [],
    bigfive: {
      profile:'individual',
      openness:0.8,
      conscientiousness:0.6,
      extraversion:0.5,
      agreeableness:0.7,
      neuroticism:0.3,
      confidence:0.8
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness, conscientiousness: bf.conscientiousness, extraversion: bf.extraversion,
    agreeableness: bf.agreeableness, neuroticism: bf.neuroticism, confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 14:01:15
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_032',
    emotions: [
      {name:'contentment', valence:0.7, arousal:0.4, confidence:0.9},
      {name:'motivation', valence:0.8, arousal:0.5, confidence:0.8},
      {name:'calm', valence:0.6, arousal:0.3, confidence:0.8},
      {name:'anxiety', valence:-0.4, arousal:0.6, confidence:0.7}
    ],
    distortions: [],
    stages: [
      {name:'autonomy_vs_shame_doubt', confidence:0.8}
    ],
    attachments: [
      {name:'secure', confidence:0.8}
    ],
    defenses: [],
    schemas: [],
    bigfive: {
      profile:'individual',
      openness:0.8,
      conscientiousness:0.6,
      extraversion:0.5,
      agreeableness:0.7,
      neuroticism:0.3,
      confidence:0.8
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 14:01:41
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_033',
    emotions: [
      {name:'Contentment', valence:0.7, arousal:0.4, confidence:0.9},
      {name:'Motivation', valence:0.8, arousal:0.5, confidence:0.8},
      {name:'Calm', valence:0.6, arousal:0.3, confidence:0.8},
      {name:'Anxiety', valence:-0.4, arousal:0.6, confidence:0.7}
    ],
    distortions: [],
    stages: [{name:'Autonomy_vs_shame/doubt', confidence:0.8}],
    attachments: [{name:'Secure', confidence:0.8}],
    defenses: [],
    schemas: [],
    bigfive: {profile:'individual', openness:0.8, conscientiousness:0.6, extraversion:0.5, agreeableness:0.7, neuroticism:0.3, confidence:0.8}
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 14:02:07
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_034',
    emotions: [
      {name:'negative', valence:-0.5, arousal:0.6, confidence:0.8}
    ],
    distortions: [
      {type:'Magnification', confidence:0.6}
    ],
    stages: [
      {name:'Industry_vs_inferiority', confidence:0.5}
    ],
    attachments: [
      {name:'Anxious_preoccupied', confidence:0.7}
    ],
    defenses: [
      {name:'None', confidence:0.6}
    ],
    schemas: [
      {name:'Defectiveness_shame', confidence:0.6}
    ],
    bigfive: {
      profile:'individual',
      openness:0.5,
      conscientiousness:0.7,
      extraversion:0.4,
      agreeableness:0.6,
      neuroticism:0.7,
      confidence:0.7
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 14:02:26
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_035',
    emotions: [
      {name:'Anxiety', valence:-0.4, arousal:0.7, confidence:0.8},
      {name:'Sadness', valence:-0.6, arousal:0.5, confidence:0.7},
      {name:'Relief', valence:0.5, arousal:0.3, confidence:0.7},
      {name:'Negative Valence', valence:-0.5, arousal:0.6, confidence:0.8}
    ],
    distortions: [
      {type:'Magnification', confidence:0.6}
    ],
    stages: [
      {name:'Industry_vs_inferiority', confidence:0.5}
    ],
    attachments: [
      {name:'Anxious_preoccupied', confidence:0.7}
    ],
    defenses: [],
    schemas: [
      {name:'Defectiveness_shame', confidence:0.6}
    ],
    bigfive: {
      profile:'individual',
      openness:0.5,
      conscientiousness:0.7,
      extraversion:0.4,
      agreeableness:0.6,
      neuroticism:0.7,
      confidence:0.7
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence
  }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 14:02:54
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_036',
    emotions: [
             {name:'Frustration', valence:-0.7, arousal:0.6, confidence:0.8},
             {name:'Disappointment', valence:-0.6, arousal:0.5, confidence:0.7},
             {name:'Relief', valence:0.4, arousal:0.3, confidence:0.6},
             {name:'Anxiety', valence:-0.5, arousal:0.7, confidence:0.7} ],
    distortions: [ {type:'All or nothing thinking', confidence:0.7},
             {type:'Catastrophizing', confidence:0.6},
             {type:'Overgeneralization', confidence:0.5} ],
    stages: [ {name:'Identity_vs_role_confusion', confidence:0.7} ],
    attachments: [ {name:'Anxious_preoccupied', confidence:0.6} ],
    defenses: [ {name:'Rationalization', confidence:0.6} ],
    schemas: [ {name:'Defectiveness_shame', confidence:0.7},
             {name:'Failure', confidence:0.6} ],
    bigfive: {
             profile:'individual',
             openness:0.6,
             conscientiousness:0.4,
             extraversion:0.5,
             agreeableness:0.5,
             neuroticism:0.7,
             confidence:0.7}
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness,
    conscientiousness: bf.conscientiousness,
    extraversion: bf.extraversion,
    agreeableness: bf.agreeableness,
    neuroticism: bf.neuroticism,
    confidence: bf.confidence }]->(b)
);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 14:03:24
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_037',
    emotions: [
      {name:'Frustration', valence:-0.4, arousal:0.5, confidence:0.8},
      {name:'Anxiety', valence:-0.5, arousal:0.6, confidence:0.9},
      {name:'Relief', valence:0.3, arousal:0.4, confidence:0.7},
      {name:'Confusion', valence:-0.2, arousal:0.3, confidence:0.7}
    ],
    distortions: [
      {type:'Catastrophizing', confidence:0.8},
      {type:'Overgeneralization', confidence:0.7},
      {type:'Personalization', confidence:0.6}
    ],
    stages: [
      {name:'Industry_vs_Inferiority', confidence:0.8}
    ],
    attachments: [
      {name:'Anxious_preoccupied', confidence:0.8}
    ],
    defenses: [
      {name:'Rationalization', confidence:0.7}
    ],
    schemas: [
      {name:'Emotional_deprivation', confidence:0.6}
    ],
    bigfive: {
      profile:'individual',
      openness:0.8,
      conscientiousness:0.9,
      extraversion:0.5,
      agreeableness:0.6,
      neuroticism:0.8,
      confidence:0.8
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness, conscientiousness: bf.conscientiousness, extraversion: bf.extraversion,
    agreeableness: bf.agreeableness, neuroticism: bf.neuroticism, confidence: bf.confidence
  }]->(b)
);

// ============================================================================
