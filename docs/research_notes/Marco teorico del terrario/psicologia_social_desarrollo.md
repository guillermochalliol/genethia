# Social, Developmental and Educational Psychology Framework for the LLM Village Terrarium

Note on verification: citations marked [V] were checked against a fetched page this session. Citations marked [K] are standard references given with their canonical DOI or publisher link from prior knowledge; their URLs were not fetched this session and should be spot-checked before publication (the user requires verified data). No citation has been invented, but [K] items carry slightly more risk of a wrong page number or DOI.

## Group influence: Asch, Sherif, Moscovici, Janis, Milgram / Haslam & Reicher, Zimbardo / Le Texier

### Takeaway
The classic influence findings are uneven. Asch conformity and minority influence are fairly robust. Milgram replicates in part but is now read as "engaged followership" (identification with the leader's cause), not blind obedience. The Stanford Prison Experiment (SPE) is methodologically discredited and should be used only as a cautionary tale about demand characteristics, never as a baseline. LLM tests already show strong Asch-like conformity, especially in small and uncertain models, so the terrarium's 3B-8B agents are a high-conformity population by default.

### Cited Findings

**Asch: conformity**
- Core claim: people sometimes give an obviously wrong answer in a line-judgment task when a unanimous majority gives it. A single dissenting ally greatly reduces conformity. Key paper: Asch, S. E. (1956). Studies of independence and conformity: I. A minority of one against a unanimous majority. *Psychological Monographs, 70*(9), 1-70. — [K] [doi:10.1037/h0093718](https://doi.org/10.1037/h0093718)
- LLM test: Zhu, Zhang, Stafford, Collier & Vlachos, "Conformity in Large Language Models" (arXiv 2410.12428, v2 May 2025). All tested LLMs conformed to the majority, whether or not their first answer was correct. Conformity was higher when the model was uncertain and lower in instruction-tuned models. A more natural-sounding majority increased conformity. Two interventions, "Devil's Advocate" and "Question Distillation", reduced it. — [V] [alphaXiv](https://www.alphaxiv.org/abs/2410.12428v2)
- LLM test: Choi et al. (2025), "An Empirical Study of Group Conformity in Multi-Agent Systems" (arXiv 2506.01332). Across more than 2,500 debates, neutral agents conformed to the larger side, and conformity rose at 4:1 and 8:1 ratios. Stronger ("more intelligent") agents swayed the neutral agent even when outnumbered, and this effect (η²p≈0.17) was larger than the majority-size effect (η²p≈0.07). The smallest Qwen models (3B, 7B) were the most prone to follow the stronger side. The authors observed polarization and "spiral of silence" behavior. — [V] [arXiv](https://arxiv.org/html/2506.01332v1)

**Sherif: norm formation and Robbers Cave**
- Core claim (autokinetic studies): in ambiguous situations, groups converge on a shared frame of reference, and that norm persists in individuals afterward. Key book: Sherif, M. (1936). *The Psychology of Social Norms*. Harper. — [K] (no URL fetched)
- Core claim (Robbers Cave): competition for scarce resources produces intergroup hostility, and superordinate goals reduce it (realistic conflict theory). Key book: Sherif, M., Harvey, O. J., White, B. J., Hood, W. R., & Sherif, C. W. (1961). *Intergroup Conflict and Cooperation: The Robbers Cave Experiment*. University of Oklahoma Book Exchange. — [K]
- Critique: Gina Perry, *The Lost Boys: Inside Muzafer Sherif's Robbers Cave Experiment* (Scribe, 2018). Based on archival work, it documents the 1953 Middle Grove study, in which the boys did not turn against each other as planned, and questions the researchers' manipulation of the camps. — [V, search result only] [Scribe Publications](https://scribepublications.com/books/the-lost-boys); [CBC](https://amp.cbc.ca/lite/story/1.5143768)
- LLM analogue of norm formation: Flint Ashery, Aiello & Baronchelli (2025), "Emergent social conventions and collective bias in LLM populations", *Science Advances*, doi:10.1126/sciadv.adu9368. In populations of 24-200 agents playing a naming game, shared conventions emerged with no central coordination. Collective biases appeared that could not be traced to any individual agent. Committed minorities could tip the whole population to a new convention. Results held for Llama-2/3/3.1-70B and Claude-3.5-Sonnet. — [V] [City St George's](https://www.citystgeorges.ac.uk/news-and-events/news/2025/may/Groups-AI-agents-spontaneously-form-own-social-norms-without-human-help-suggests-study); [arXiv 2410.08948](https://arxiv.org/html/2410.08948v2)

**Moscovici: minority influence**
- Core claim: a consistent minority can shift a majority, often through private or latent change rather than public compliance (conversion theory). In the blue/green slide study, a consistent confederate minority produced about 8% "green" responses, against roughly 1% in controls; an inconsistent minority had much less effect. Key paper: Moscovici, S., Lage, E., & Naffrechoux, M. (1969). Influence of a consistent minority on the responses of a majority in a color perception task. *Sociometry, 32*(4), 365-380. — [K] [doi:10.2307/2786541](https://doi.org/10.2307/2786541). The percentages are standard textbook figures; see summary at [tutor2u](https://www.tutor2u.net/psychology/reference/minority-influence-consistency-and-commitment) [V, search result only].
- Meta-analysis: Wood, W., Lundgren, S., Ouellette, J. A., Busceme, S., & Blackstone, T. (1994). Minority influence: A meta-analytic review of social influence processes. *Psychological Bulletin, 115*(3), 323-345. — [K] [doi:10.1037/0033-2909.115.3.323](https://doi.org/10.1037/0033-2909.115.3.323). Not fetched; my search did not retrieve it.
- LLM link: the Baronchelli committed-minority tipping result above is the closest LLM test of Moscovici-style consistency. — [V] [City St George's](https://www.citystgeorges.ac.uk/news-and-events/news/2025/may/Groups-AI-agents-spontaneously-form-own-social-norms-without-human-help-suggests-study)

**Janis: groupthink**
- Core claim: cohesive, insulated groups with directive leaders seek concurrence and stop evaluating alternatives realistically. Key book: Janis, I. L. (1972/1982). *Victims of Groupthink* / *Groupthink: Psychological Studies of Policy Decisions and Fiascoes* (2nd ed.). Houghton Mifflin. — [K]
- Contested: a 1998 special issue of *Organizational Behavior and Human Decision Processes* (vol. 73, issues 2-3) re-examined the model. Kramer (1998, pp. 236-271) revisited the Bay of Pigs and Vietnam cases; the issue also includes Esser (1998), "Alive and well after 25 years: A review of groupthink research", pp. 116-141. Empirical support for the full causal model is weak and mixed. — [V for the Kramer citation] [IDEAS/RePEc](https://ideas.repec.org/a/eee/jobhdp/v73y1998i2-3p236-271.html). The verdict "weak/mixed support" comes from Esser's review and is [K]; I could not fetch its abstract.
- LLM analogue: Liang et al., "Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate" (EMNLP 2024; arXiv 2305.19118). It defines "Degeneration-of-Thought": once confident, an LLM cannot generate novel thoughts through self-reflection. A debate with a judge counters this. — [V] [arXiv](https://arxiv.org/html/2305.19118v3); [ACL Anthology](https://aclanthology.org/2024.emnlp-main.992)

**Milgram, and Haslam & Reicher's engaged followership**
- Core claim: in Milgram's Experiment 1, 26 of 40 participants (65%) obeyed to the maximum 450V. Key paper: Milgram, S. (1963). Behavioral study of obedience. *Journal of Abnormal and Social Psychology, 67*(4), 371-378. — [K] [doi:10.1037/h0040525](https://doi.org/10.1037/h0040525). The 26/40 figure is confirmed in Aher et al. (below). [V]
- Reinterpretation: Reicher, Haslam & Smith (2012), "Working toward the experimenter: Reconceptualizing obedience within the Milgram paradigm as identification-based followership", *Perspectives on Psychological Science*. Participants were engaged followers who identified with the experimenter's scientific project, weighed it against the learner's appeal, and acted accordingly ("Followership of this form is not thoughtless"). The article cites Packer (2008) on where participants stopped and Burger (2009) on disobedience under a direct order. — [V] [APS Observer](https://www.psychologicalscience.org/publications/observer/obsonline/not-obedience-but-followership.html); [St Andrews portal](https://research-portal.st-andrews.ac.uk/en/publications/working-toward-the-experimenter-reconceptualizing-obedience-withi/)
- Related: Haslam, Reicher & Birney (2014), "Nothing by mere authority: Evidence that in an experimental analogue of the Milgram paradigm participants are motivated not by orders but by appeals to science", *Journal of Social Issues, 70*(3). The often-cited finding is that the only true order ("You have no other choice, you must go on") led to more disobedience, not less. — [K] I could not verify this through a fetched page. Burger's disobedience-under-order point is confirmed in the APS article above.
- LLM test: Aher, Arriaga & Kalai (2023), "Using Large Language Models to Simulate Multiple Humans and Replicate Human Subject Studies", ICML 2023 (PMLR 202). In the Milgram simulation, 75 of 100 simulated participants obeyed to the end, against 26 of 40 in the original, so the models were more compliant than humans. The paper also reports a "hyper-accuracy distortion" in aligned models. — [V] [arXiv](https://arxiv.org/html/2208.10264v5); [PMLR](https://proceedings.mlr.press/v202/aher23a/aher23a.pdf)

**Zimbardo SPE and its debunking**
- Original: Haney, C., Banks, C., & Zimbardo, P. (1973). Interpersonal dynamics in a simulated prison. *International Journal of Criminology and Penology, 1*, 69-97. — [K]
- Debunking: Le Texier, T. (2019). Debunking the Stanford Prison Experiment. *American Psychologist, 74*(7), 823-839. — [V] [Stafforini catalog](https://stafforini.com/works/le-texier-2019-debunking-stanford-prison/); [PDF (gwern)](https://www.Gwern.net/doc/psychology/2019-letexier.pdf). The book version is *Histoire d'un mensonge: Enquête sur l'expérience de Stanford* (Zones, 2018). [K] Le Texier's archival case, as he presents it: guards were coached toward toughness, demand characteristics were strong, and the results were pre-shaped. — [V, podcast summary] [Rationally Speaking #241](https://rationallyspeakingpodcast.org/241-debunking-the-stanford-prison-experiment-thibault-le-texier/)
- Reinterpretation: Haslam, S. A., Reicher, S. D., & Van Bavel, J. J. (2019). Rethinking the nature of cruelty: The role of identity leadership in the Stanford Prison Experiment. *American Psychologist, 74*(7), 809-822. It argues that guard cruelty reflected Zimbardo's identity leadership (cultivating a "tough guard" identity), not spontaneous role conformity. — [V] [PDF, Van Bavel lab](https://vanbavellab.hosting.nyu.edu/documents/Haslam.etal.2019.AmPsych.pdf); [St Andrews](https://research-portal.st-andrews.ac.uk/en/publications/rethinking-the-nature-of-cruelty-the-role-of-identity-leadership-/)

### Inferences
- **Prediction for the terrarium:** 3B-8B agents will conform heavily, especially to agents from bigger or "smarter-sounding" models (Choi et al.), and to anyone perceived as an authority (Aher et al.). Without governance, expect fast norm lock-in and "spiral of silence" collapse of dissent.
- **Operationalizations:**
  - *Asch probe:* plant k confederate agents who give a wrong answer on a verifiable task. Measure the flip rate of the naive agent. Manipulate majority size (1-7), unanimity (with or without one dissenting ally, Asch's key moderator), and the confederates' model family or size.
  - *Moscovici probe:* an implanted minority (1-2 agents) argues consistently, or inconsistently, for a correct but unpopular solution. Measure public adoption, and latent adoption on later private tasks.
  - *Groupthink index:* number of distinct alternatives raised before a decision; rate at which the devil's advocate's objections are ignored; decision error on verifiable tasks. Compare villages with a rotating devil's advocate, a fixed one, and none.
  - *Followership versus obedience (unjust leader):* the leader orders a harmful or cheating action, framed either as an order ("you have no choice") or as an appeal to a shared mission. Haslam and Reicher predict that mission framing gets more compliance than direct orders. This is testable and rarely tested in LLMs.
  - *SPE:* do not replicate it as a "role induces cruelty" baseline. Use it to test demand characteristics: compare guard-like roles given neutral briefings with ones given "be tough" leader briefings (Haslam et al. 2019).

### Gaps
- No fetched source verified the "prod 4 leads to disobedience" result of Haslam, Reicher & Birney 2014, or the Wood et al. (1994) meta-analytic effect sizes.
- I found no LLM study replicating Sherif's autokinetic paradigm directly, or a Robbers Cave design with superordinate goals. This is an open niche.
- A 2026 arXiv paper titled "Recognition, Simulation, and Refusal: A Contamination-Aware Study of Classic Psychological Effects in LLM Agents" (arXiv 2609.22090) looks highly relevant, since models may recognize famous paradigms, but its PDF could not be read. [Link](https://arxiv.org/pdf/2609.22090)

## Social identity and intergroup relations: Tajfel & Turner, minimal groups, Allport's contact hypothesis

### Takeaway
Social identity theory predicts in-group favoritism even when group labels are trivial, and LLM agents already show it in minimal-group allocation tasks. Contact reduces prejudice on average (meta-analysis of 515 studies), but the effect is weaker in rigorous randomized studies, and Allport's conditions are rarely tested. Immigrant integration in the terrarium is therefore a strong test case.

### Cited Findings
- Minimal group paradigm: Tajfel, H., Billig, M. G., Bundy, R. P., & Flament, C. (1971). Social categorization and intergroup behaviour. *European Journal of Social Psychology, 1*(2), 149-178. — [K] [doi:10.1002/ejsp.2420010202](https://doi.org/10.1002/ejsp.2420010202)
- Social identity theory: Tajfel, H., & Turner, J. C. (1979). An integrative theory of intergroup conflict. In W. G. Austin & S. Worchel (Eds.), *The Social Psychology of Intergroup Relations* (pp. 33-47). Brooks/Cole. — [K]
- Contact hypothesis: Allport, G. W. (1954). *The Nature of Prejudice*. Addison-Wesley. Optimal conditions: equal status, common goals, intergroup cooperation, and institutional support. — [K]
- Meta-analysis: Pettigrew, T. F., & Tropp, L. R. (2006). A meta-analytic test of intergroup contact theory. *Journal of Personality and Social Psychology, 90*(5), 751-783. It covers 515 studies, and contact typically reduces prejudice. — [V] [PubMed 16737372](https://pubmed.ncbi.nlm.nih.gov/16737372/)
- Critique: Paluck, E. L., Green, S. A., & Green, D. P. (2019). The contact hypothesis re-evaluated. *Behavioural Public Policy, 3*(2), 129-158. They reviewed 27 randomized studies with delayed outcomes. The evidence is consistent with prejudice reduction, but effects are substantially weaker for ethnic or racial prejudice, and few studies test Allport's conditions. — [V] [IDEAS/RePEc](https://ideas.repec.org/a/cup/bpubpo/v3y2019i02p129-158_00.html)
- LLM test: Hu, T., Kyrychenko, Y., et al. (2025). Generative language models exhibit social identity biases. *Nature Computational Science* (s43588-024-00741-1). They tested more than 70 models. Base models show human-like "we" positivity and "they" negativity, and instruction-tuned models show much less. Fine-tuning on partisan tweets made models 3-5 times more biased, and filtering tribal language reduced bias. — [V] [Gates Cambridge](https://gatescambridge.org/about/news/are-ai-models-as-divided-as-we-are); [arXiv 2310.15819](https://arxiv.org/pdf/2310.15819)
- LLM test (minimal group): Wang et al. (2026), "When Agents See Humans as the Outgroup: Belief-Dependent Bias in LLM-Powered Agents" (arXiv 2601.00240). Using a Tajfel-style 2x13 allocation matrix, agents favored their arbitrary in-group. Framing the out-group as human removed the bias, but belief-poisoning of memory or profile restored it. — [V] [arXiv](https://arxiv.org/html/2601.00240v2)

### Inferences
- **Prediction:** villages will show in-group favoritism toward their own villagers and toward agents of the same base-model family, even with arbitrary labels. Immigrants, especially from other model families, start as out-group. Base (non-instruct) models in the genome pool should be more tribal (Hu et al.).
- **Operationalizations:**
  - *Minimal-group probe:* periodic Tajfel matrix allocations (in-group or out-group by village, by model family, and by arbitrary color tag). Measure favoritism (FAV) and maximum-difference (MD) strategy.
  - *Contact manipulation:* immigrant integration under Allport conditions (equal status, shared verifiable goal, leader endorsement) versus integration as low-status newcomers. Outcome measures: allocation bias, trust ratings, immigrant task success, and "mate choice" across groups through the affinity function.
  - *Realistic conflict (Sherif):* scarcity of shared resources between villages, followed by a superordinate goal task that neither village can solve alone.
  - *Memory integrity:* the belief-poisoning result implies that the historian or memory role is an attack surface for identity manipulation, which is relevant to the villain condition.

### Gaps
- No LLM study found that tests Allport's contact conditions or superordinate goals between agent groups.

## Cooperation and trust: Axelrod, Edmondson, Deci & Ryan, Festinger, Bandura

### Takeaway
Reciprocity-based cooperation (Axelrod) is well established in theory. LLM societies can evolve cooperation culturally, but this depends strongly on the model and the random seed, and most models over-exploit commons. Psychological safety and self-determination theory supply measurable constructs for the "humanity" condition. Cognitive dissonance's classic induced-compliance effect failed a large 2024 multilab replication, so it should be treated cautiously. Ego depletion also failed a multilab replication and should not be used as a mechanism.

### Cited Findings
- **Axelrod:** Axelrod, R., & Hamilton, W. D. (1981). The evolution of cooperation. *Science, 211*(4489), 1390-1396. — [K] [doi:10.1126/science.7466396](https://doi.org/10.1126/science.7466396). Book: Axelrod, R. (1984). *The Evolution of Cooperation*. Basic Books. — [K] Tit-for-tat won the tournaments by being nice, retaliatory, forgiving and clear.
- LLM test: Akata, E., Schulz, L., Coda-Forno, J., Oh, S. J., Bethge, M., & Schulz, E. (2025). Playing repeated games with large language models. *Nature Human Behaviour, 9*(7), 1380-1390. doi:10.1038/s41562-025-02172-y. LLMs did well in self-interested games (the iterated Prisoner's Dilemma family) and poorly in coordination games (Battle of the Sexes). Information about the opponent and "social chain-of-thought" improved coordination. — [V] [IDEAS/RePEc](https://ideas.repec.org/a/nat/nathum/v9y2025i7d10.1038_s41562-025-02172-y.html)
- LLM test: Vallinder, A., & Hughes, E. (2024). Cultural evolution of cooperation among LLM agents (arXiv 2412.10270; AAMAS 2025). In a multi-generation Donor Game, Claude 3.5 Sonnet societies cooperated best, ahead of Gemini 1.5 Flash and GPT-4o. Only Claude benefited from costly punishment, and outcomes varied across seeds. — [V] [arXiv](https://arxiv.org/abs/2412.10270v1)
- LLM test: Piatti, Jin, Kleiman-Weiner, Schölkopf, Sachan & Mihalcea (2024), "Cooperate or Collapse: Emergence of Sustainable Cooperation in a Society of LLM Agents" (GovSim, NeurIPS 2024). Only the most powerful LLMs reached a sustainable equilibrium in the commons, and the best survival rate was below 54%. "Universalization" moral reasoning improved sustainability. — [V] [arXiv](https://arxiv.org/abs/2404.16698v4); [NeurIPS](https://neurips.cc/virtual/2024/poster/96895)
- **Edmondson:** Edmondson, A. (1999). Psychological safety and learning behavior in work teams. *Administrative Science Quarterly, 44*(2), 350-383. Psychological safety is a shared belief that the team is safe for interpersonal risk-taking, and it predicts learning behavior, which mediates performance. — [V, search result] [Harvard DASH](https://dash.harvard.edu/entities/publication/13a7b031-0fdd-45ec-a7e0-2b80e2bc679f); [MIT PDF](https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Group_Performance/Edmondson%20Psychological%20safety.pdf). Book: Edmondson, A. C. (2018). *The Fearless Organization*. Wiley. — [K]
- **Self-determination theory:** Ryan, R. M., & Deci, E. L. (2000). Self-determination theory and the facilitation of intrinsic motivation, social development, and well-being. *American Psychologist, 55*(1), 68-78. It identifies three basic needs: autonomy, competence, relatedness. — [K] [doi:10.1037/0003-066X.55.1.68](https://doi.org/10.1037/0003-066X.55.1.68). Book: Ryan, R. M., & Deci, E. L. (2017). *Self-Determination Theory: Basic Psychological Needs in Motivation, Development, and Wellness*. Guilford. — [K]
- **Festinger:** Festinger, L. (1957). *A Theory of Cognitive Dissonance*. Stanford University Press; Festinger, L., & Carlsmith, J. M. (1959). Cognitive consequences of forced compliance. *JASP, 58*, 203-210. — [K]
- Replication: Vaidis, D. C., et al. (2024). A multilab replication of the induced-compliance paradigm of cognitive dissonance. *Advances in Methods and Practices in Psychological Science* (doi:10.1177/25152459231213375). It involved 39 labs in 19 countries and about 4,900 participants. The effect of choice on attitude change did not replicate, though writing a counter-attitudinal essay did shift attitudes compared with a neutral essay. — [V] [APS Observer](https://www.psychologicalscience.org/observer/multilab-replication-cognitive-dissonance); [FORRT](https://forrt.org/flora-replication-atlas/doi/10.1177/25152459231213375/)
- LLM test: Lehr, Saichandran, Harmon-Jones, Vitali & Banaji (2025), "Kernels of selfhood: GPT-4o shows humanlike patterns of cognitive dissonance moderated by free choice" (PNAS; arXiv 2502.07088). GPT-4o's attitude toward Putin shifted after it wrote an essay, more so under an illusion of choice. — [V, search result] [arXiv](https://arxiv.org/abs/2502.07088v1); [Harvard Gazette](https://news.harvard.edu/gazette/story/2025/07/can-ai-be-as-irrational-as-we-are-or-even-more-so). Irony: the free-choice effect that GPT-4o showed failed to replicate in humans (Vaidis 2024).
- **Ego depletion (replication-crisis example):** Hagger, M. S., Chatzisarantis, N. L. D., et al. (2016). A multilab preregistered replication of the ego-depletion effect. *Perspectives on Psychological Science, 11*(4), 546-573. It involved 23 labs, and the effect was close to zero. — [V, search result] [Tilburg portal](https://research.tilburguniversity.edu/en/publications/a-multi-lab-pre-registered-replication-of-the-ego-depletion-effec/); [Discover](https://discovermagazine.com/mind/the-end-of-ego-depletion-theory). The 23-lab count and near-zero effect are [K] details.
- **Bandura:** Bandura, A. (1977). *Social Learning Theory*. Prentice Hall; Bandura, Ross & Ross (1961), Bobo doll, *JASP, 63*, 575-582. Observational learning depends on attention, retention, reproduction and motivation, including vicarious reinforcement. — [K]
- Generative agents as social simulation baseline: Park, J. S., et al. (2023). Generative Agents: Interactive Simulacra of Human Behavior. UIST 2023. — [V, search result] [arXiv 2304.03442](https://arxiv.org/pdf/2304.03442)

### Inferences
- **Prediction:** small 3B-8B models are below the capability threshold that GovSim and Vallinder & Hughes found necessary for stable cooperation. The "no governance" condition is likely to collapse under scarcity, and "rules only" or "humanity" conditions may be needed for cooperation to survive at all. Seed variance will be large, so many replicate runs per condition are needed.
- **Operationalizations:**
  - *Axelrod:* embedded iterated PD and Donor Game rounds. Classify strategies (TFT, generous TFT, always-defect) from move logs, and measure the forgiveness rate after defection.
  - *Edmondson:* a psychological-safety index computed from logs: rate of error admission, rate of questions asked, whether the questioner's dissent is punished or rewarded, and the "psychologist" agent's ratings. Edmondson's 7-item scale could be adapted as a self-report probe, but self-report from LLMs needs validation against behavior.
  - *SDT in the "humanity" condition:* manipulate autonomy (choice of task or role versus assigned), competence (calibrated feedback on verifiable tasks), and relatedness (persistent pairings or affinity bonds). Measure persistence on hard tasks, cheating under temptation, and task success. SDT predicts that autonomy support lowers cheating and raises persistence.
  - *Dissonance:* after an agent cheats or obeys an unjust leader, measure whether its stated values or constitution interpretation drift toward justifying the act. Do not frame this as a choice-moderated effect, given Vaidis 2024.
  - *Bandura:* newborns observe a model agent rewarded or punished for cheating. Measure imitation, and manipulate the model's status (elder or leader versus peer).

### Gaps
- No LLM test of psychological safety in multi-agent teams was found in this pass (searches not exhausted).
- I found no direct test of SDT needs in LLM agents.

## Developmental and educational theory: Vygotsky, Piaget, Bruner, Tomasello, Lave & Wenger — raising newborn agents

### Takeaway
The developmental frameworks converge on one recommendation. Newborn agents should be integrated through guided participation in real, verifiable tasks. Elders should scaffold within the newborn's zone of proximal development and fade support as competence grows. Legitimate peripheral participation means starting at low-stakes but authentic positions such as verifier-assistant or historian-assistant. Shared intentionality, meaning joint goals and norms, is the target, not imitation alone. This is the part of the design a pedagogical psychologist such as Aneley would scrutinize most.

### Cited Findings
- **Vygotsky:** Vygotsky, L. S. (1978). *Mind in Society: The Development of Higher Psychological Processes* (M. Cole et al., Eds.). Harvard University Press. The zone of proximal development (ZPD) is the gap between what a learner can do alone and what it can do with guidance. Higher mental functions appear first between people, then within the individual. — [K] [Harvard UP](https://www.hup.harvard.edu/books/9780674576292)
- **Scaffolding:** Wood, D., Bruner, J. S., & Ross, G. (1976). The role of tutoring in problem solving. *Journal of Child Psychology and Psychiatry, 17*(2), 89-100. It names six tutor functions: recruitment, reduction of degrees of freedom, direction maintenance, marking critical features, frustration control, and demonstration. — [V] [PubMed 932126](https://pubmed.ncbi.nlm.nih.gov/932126/). The list of six functions is [K].
- **Bruner:** Bruner, J. S. (1960). *The Process of Education* (the spiral curriculum); Bruner, J. S. (1996). *The Culture of Education*. Harvard University Press. — [K]
- **Piaget:** Piaget, J. (1952). *The Origins of Intelligence in Children*. International Universities Press. Learning happens through assimilation, accommodation and equilibration, and cognitive conflict drives development. Socio-cognitive conflict between peers is a later extension (Doise & Mugny). — [K]
- **Tomasello:** Tomasello, M. (2019). *Becoming Human: A Theory of Ontogeny*. Harvard University Press (Belknap). It argues that uniquely human cognition and sociality grow out of shared intentionality: joint attention and joint goals emerge at about 9 months, and collective intentionality (norms, conventions) at about 3 years. — [V] [Duke Evolutionary Anthropology](https://evolutionaryanthropology.duke.edu/books/becoming-human-theory-ontogeny); [Cambridge review](https://resolve.cambridge.org/core/journals/philosophy/article/abs/becoming-human-a-theory-of-ontogeny-by-michael-tomasello-cambridge-mass-harvard-university-press-2019/AF7CDE9A832032F7584DF715FF2D2C83). The age milestones are [K].
- Tomasello, M., Carpenter, M., Call, J., Behne, T., & Moll, H. (2005). Understanding and sharing intentions: The origins of cultural cognition. *Behavioral and Brain Sciences, 28*(5), 675-691. — [K] [doi:10.1017/S0140525X05000129](https://doi.org/10.1017/S0140525X05000129). Also Tomasello, M. (1999). *The Cultural Origins of Human Cognition*. Harvard UP, on the "ratchet effect" of cumulative culture. — [K]
- **Lave & Wenger:** Lave, J., & Wenger, E. (1991). *Situated Learning: Legitimate Peripheral Participation*. Cambridge University Press. doi:10.1017/CBO9780511815355. Newcomers become full members of a community of practice by moving from peripheral but legitimate participation toward full participation. — [V] [DOI](https://doi.org/10.1017/CBO9780511815355); [New Learning summary](https://newlearningonline.com/new-learning/chapter-6/lave-and-wenger-on-situated-learning). Also Rogoff, B. (1990). *Apprenticeship in Thinking*. Oxford UP. — [K]
- LLM work: "A Theory of Adaptive Scaffolding for LLM-Based Pedagogical Agents" (arXiv 2508.01503; AAAI). It concerns LLM tutors for humans, not agent-to-agent upbringing. — [V, search result] [arXiv](https://arxiv.org/abs/2508.01503)
- LLM cultural transmission: Perez, J., Léger, C., Ovando-Tellez, M., Foulon, C., Dussauld, J., Oudeyer, P.-Y., & Moulin-Frier, C. (2024). Cultural evolution in populations of Large Language Models (arXiv 2403.08882). It is a framework for transmission chains or networks with personality prompts across generations, and it has no explicit selection. — [V] [arXiv](https://arxiv.org/html/2403.08882v1). Also Perez et al., "When LLMs Play the Telephone Game: Cultural Attractors…" (ICLR 2025). — [V, search result] [mlanthology](https://mlanthology.org/iclr/2025/perez2025iclr-llms)
- LLM emergent roles and culture: Altera.AL (2024), "Project Sid: Many-agent simulations toward AI civilization" (arXiv 2411.00114). In 30-agent Minecraft villages, roles emerged autonomously (farmer, guard, and others), and agents without social modules did not specialize. Agents followed a democratically amended tax law. A seeded religion spread across towns in a 500-agent run. — [V] [arXiv](https://arxiv.org/html/2411.00114v1)

### Inferences
- **How to raise newborn agents (operationalization):**
  1. *ZPD calibration:* estimate the newborn's solo success on a graded task ladder, then assign tasks one level above its solo level with elder hints. Measure the gap between solo and assisted performance, which is the ZPD width.
  2. *Scaffolding with fading:* elders provide Wood-Bruner-Ross functions, with hint density decaying over time. Compare against no scaffolding (sink or swim) and against permanent scaffolding (over-helping). Prediction: fading beats both on later independent performance.
  3. *Legitimate peripheral participation:* newborns enter as apprentices to the verifier or historian (low risk, authentic work), then rotate toward core roles. Compare against immediate assignment to a core role.
  4. *Shared intentionality (Tomasello):* measure whether newborns adopt joint goals ("we" framing), enforce norms on third parties (third-party punishment of cheaters), and pass conventions to later newborns. This is the cumulative-culture "ratchet".
  5. *Socio-cognitive conflict (Piaget):* pair newborns with peers who hold a different wrong answer, and compare learning against elder instruction.
  6. *Bandura:* elders are models, and their observed reward or punishment shapes newborn imitation.
- **Risk:** elders transmitting errors or unjust norms (cultural attractors, Perez et al.) and conformity pressure on small newborn models. The historian or memory role should keep records of what was verified, so that culture is not drift.
- The Vygotskian frame implies a measurable distinction. A newborn whose behavior changes only while the elder is present shows performance under support. A newborn whose solo performance improves after support is removed shows internalization. The second is what should count as "education".

### Gaps
- I found no LLM study of agent-to-agent apprenticeship or ZPD-calibrated upbringing of new agents in a society. This appears to be an open area and a potential contribution.
- I did not verify a specific source for Doise & Mugny's socio-cognitive conflict work.

## Group size and structure: Dunbar and critiques, Tuckman stages

### Takeaway
Dunbar's 150 is contested. A 2021 reanalysis gives 95% confidence intervals of 2-520 for humans, so it has little bearing on 8-12-agent villages. Inner "support clique" layers of about 5 and "sympathy group" layers of about 12-15 are a more relevant (but also debated) reference. Tuckman's stages offer a descriptive coding scheme for village life-cycles but are not a validated causal model.

### Cited Findings
- Dunbar, R. I. M. (1992). Neocortex size as a constraint on group size in primates. *Journal of Human Evolution, 22*(6), 469-493. — [K] [doi:10.1016/0047-2484(92)90081-J](https://doi.org/10.1016/0047-2484(92)90081-J). Dunbar, R. I. M. (1993). Coevolution of neocortical size, group size and language in humans. *Behavioral and Brain Sciences, 16*(4), 681-735. — [K]
- Critique: Lindenfors, P., Wartel, A., & Lind, J. (2021). "Dunbar's number" deconstructed. *Biology Letters* (Royal Society). doi:10.1098/rsbl.2021.0158. With modern methods and data, the 95% CIs for human group size run from 2 to 520, and "it is not possible to make an estimate for humans with any precision." — [V] [Stockholm University](https://www.su.se/english/news/articles/2021-05-05-new-study-deconstructs-dunbars-number---yes-you-can-have-more-than-150-friends)
- Layers: Dunbar's layered network model (about 5, 15, 50, 150) comes from Zhou, Sornette, Hill & Dunbar (2005), *Proc. R. Soc. B, 272*, 439-444. — [K] [doi:10.1098/rspb.2004.2970](https://doi.org/10.1098/rspb.2004.2970)
- Tuckman, B. W. (1965). Developmental sequence in small groups. *Psychological Bulletin, 63*(6), 384-399. The stages are forming, storming, norming and performing; adjourning was added in Tuckman & Jensen (1977), *Group & Organization Studies, 2*(4), 419-427. — [K] [doi:10.1037/h0022100](https://doi.org/10.1037/h0022100). Tuckman's model was derived from a literature review dominated by therapy and training groups, and alternatives such as Gersick's (1988) punctuated equilibrium challenge its linear sequence. — [K]
- Project Sid used 25-50 agents per social experiment and found role specialization at 30. — [V] [arXiv](https://arxiv.org/html/2411.00114v1)

### Inferences
- An 8-12-agent village sits in the "sympathy group" range, so each agent can, in principle, track every other agent's reputation. In LLM terms the binding constraint is context window and memory, not neocortex. A testable analogue: vary village size (6 / 12 / 24) and the memory budget, then measure reputation-tracking accuracy and the stability of cooperation.
- Tuckman as a coding scheme: the "psychologist" agent or an external LLM judge labels each epoch as forming, storming, norming or performing. Key metrics: conflict rate, rate of norm proposals, task throughput. Compare how long storming lasts across governance conditions. Prediction: rules or constitution shorten storming.
- Immigrant or newborn arrival may push a village back to "storming". Measure the drop and recovery in performance after each arrival.

### Gaps
- No LLM study found that applies Tuckman coding to multi-agent societies.
- The Lindenfors critique has a published Dunbar response (2021), which I did not retrieve.

## Which theories have been tested with LLMs, and which remain untested

### Takeaway
Tested so far: conformity (Asch-like), norm or convention emergence with committed-minority tipping, Milgram obedience (in simulation), social identity and minimal-group bias, repeated games and cultural evolution of cooperation, the commons, cognitive dissonance, emergent roles and taxation, and cultural transmission chains. Largely untested: Allport's contact conditions, superordinate goals, psychological safety, SDT need-support, identity-leadership versus obedience framing, Tuckman development, and ZPD or apprenticeship-based upbringing of new agents. Contamination is a key methodological concern, since models may recognize famous paradigms.

### Cited Findings
| Theory | LLM test | Source |
|---|---|---|
| Asch conformity | Yes: Zhu et al. 2025; Choi et al. 2025 | [arXiv 2410.12428](https://www.alphaxiv.org/abs/2410.12428v2); [arXiv 2506.01332](https://arxiv.org/html/2506.01332v1) |
| Sherif norm formation / Moscovici-style tipping | Yes (conventions): Flint Ashery et al. 2025, *Sci. Adv.* | [arXiv 2410.08948](https://arxiv.org/html/2410.08948v2) |
| Milgram | Yes (simulated subjects): Aher et al. 2023 | [arXiv 2208.10264](https://arxiv.org/html/2208.10264v5) |
| Groupthink | Partly (Degeneration-of-Thought / debate): Liang et al. 2024 | [arXiv 2305.19118](https://arxiv.org/html/2305.19118v3) |
| SIT / minimal group | Yes: Hu et al. 2025; Wang et al. 2026 | [arXiv 2310.15819](https://arxiv.org/pdf/2310.15819); [arXiv 2601.00240](https://arxiv.org/html/2601.00240v2) |
| Axelrod / repeated games | Yes: Akata et al. 2025 | [RePEc](https://ideas.repec.org/a/nat/nathum/v9y2025i7d10.1038_s41562-025-02172-y.html) |
| Cultural evolution of cooperation | Yes: Vallinder & Hughes 2024 | [arXiv 2412.10270](https://arxiv.org/abs/2412.10270v1) |
| Commons / scarcity | Yes: GovSim, Piatti et al. 2024 | [arXiv 2404.16698](https://arxiv.org/abs/2404.16698v4) |
| Cognitive dissonance | Yes: Lehr et al. 2025 (GPT-4o) | [arXiv 2502.07088](https://arxiv.org/abs/2502.07088v1) |
| Emergent roles / constitution / religion | Yes: Project Sid 2024 | [arXiv 2411.00114](https://arxiv.org/html/2411.00114v1) |
| Cultural transmission chains | Yes: Perez et al. 2024 | [arXiv 2403.08882](https://arxiv.org/html/2403.08882v1) |
| Contact hypothesis (Allport conditions), superordinate goals | Not found | n/a |
| Edmondson psychological safety | Not found | n/a |
| SDT needs | Not found | n/a |
| Haslam/Reicher identity leadership vs orders | Not found | n/a |
| Tuckman stages | Not found | n/a |
| Vygotsky ZPD / Lave & Wenger apprenticeship among agents | Not found (only LLM-as-tutor-for-humans, arXiv 2508.01503) | [arXiv 2508.01503](https://arxiv.org/abs/2508.01503) |

- Contamination: a 2026 paper on "Recognition, Simulation, and Refusal" studies classic effects in LLM agents with a contamination-aware design. Its content could not be read. — [arXiv 2609.22090](https://arxiv.org/pdf/2609.22090)

### Inferences
- "Not found" means not found in this session's roughly 30 searches. It is not proof of absence, and the report should phrase it as "to our knowledge".
- Nearly all existing tests use large frontier models (GPT-4o, Claude 3.5, 70B Llamas). Results for 3B-8B heterogeneous populations are mostly unknown, apart from Choi et al.'s Qwen 3B/7B data point. That gap is itself a contribution of the terrarium.
- Contamination mitigation: disguise the paradigms (no "lines", "shocks" or "prison" wording). Use novel verifiable tasks as the conformity substrate, and check whether agents name the paradigm.

### Gaps
- I did not run exhaustive searches for psychological safety, SDT or Tuckman in multi-agent LLM work.

## Recommended core reading list (10-15 books) for the theoretical framework

### Takeaway
Fourteen books cover influence, identity, cooperation, motivation, development and critique. Pair the classics with their modern critiques (Le Texier, Perry, Haslam & Reicher) to meet the rigor requirement.

### Cited Findings
1. Asch, S. E. (1952). *Social Psychology*. Prentice-Hall. — [K]
2. Sherif, M., et al. (1961). *Intergroup Conflict and Cooperation: The Robbers Cave Experiment*. University of Oklahoma. — [K], paired with Perry, G. (2018). *The Lost Boys*. Scribe. — [V] [Scribe](https://scribepublications.com/books/the-lost-boys)
3. Moscovici, S. (1976). *Social Influence and Social Change*. Academic Press. — [K]
4. Janis, I. L. (1982). *Groupthink* (2nd ed.). Houghton Mifflin. — [K]
5. Milgram, S. (1974). *Obedience to Authority: An Experimental View*. Harper & Row. — [K], paired with Haslam, S. A., Reicher, S. D., & Platow, M. J. (2011/2020). *The New Psychology of Leadership: Identity, Influence and Power*. Psychology Press/Routledge. — [K]
6. Le Texier, T. (2018). *Histoire d'un mensonge: Enquête sur l'expérience de Stanford*. Zones/La Découverte (article version in *American Psychologist* 2019). — [V for the article] [Stafforini](https://stafforini.com/works/le-texier-2019-debunking-stanford-prison/)
7. Allport, G. W. (1954). *The Nature of Prejudice*. Addison-Wesley. — [K]
8. Tajfel, H. (1981). *Human Groups and Social Categories*. Cambridge University Press. — [K]
9. Axelrod, R. (1984). *The Evolution of Cooperation*. Basic Books. — [K]
10. Ryan, R. M., & Deci, E. L. (2017). *Self-Determination Theory*. Guilford Press. — [K]
11. Edmondson, A. C. (2018). *The Fearless Organization*. Wiley. — [K]
12. Bandura, A. (1977). *Social Learning Theory*. Prentice Hall. — [K]
13. Vygotsky, L. S. (1978). *Mind in Society*. Harvard University Press. — [K] [HUP](https://www.hup.harvard.edu/books/9780674576292)
14. Tomasello, M. (2019). *Becoming Human: A Theory of Ontogeny*. Harvard University Press. — [V] [Duke](https://evolutionaryanthropology.duke.edu/books/becoming-human-theory-ontogeny)
15. Lave, J., & Wenger, E. (1991). *Situated Learning: Legitimate Peripheral Participation*. Cambridge University Press. — [V] [doi:10.1017/CBO9780511815355](https://doi.org/10.1017/CBO9780511815355)

Optional extras: Festinger (1957) *A Theory of Cognitive Dissonance* (read alongside Vaidis et al. 2024); Tomasello (1999) *The Cultural Origins of Human Cognition*; Rogoff (1990) *Apprenticeship in Thinking*; Dunbar (1996) *Grooming, Gossip and the Evolution of Language* (read alongside Lindenfors et al. 2021).

### Inferences
- For the paper, a strong framing is "classic claim → modern critique or replication status → LLM evidence → terrarium operationalization". Every [K] item should be checked against the publisher or DOI before submission.

### Gaps
- Publisher URLs for most classic books were not fetched this session.
