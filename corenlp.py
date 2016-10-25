
mytext = "San Diego is a place in the United States of America."


from jnius import autoclass

Properties = autoclass("java.util.Properties")
StanfordCoreNLP = autoclass("edu.stanford.nlp.pipeline.StanfordCoreNLP")
CoreAnnotations = autoclass("edu.stanford.nlp.ling.CoreAnnotations")

CoreAnnotations.TokensAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$TokensAnnotation")
CoreAnnotations.SentencesAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$SentencesAnnotation")
CoreAnnotations.TextAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$TextAnnotation")
CoreAnnotations.NamedEntityTagAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$NamedEntityTagAnnotation")

CoreLabel = autoclass("edu.stanford.nlp.ling.CoreLabel")
IndexedWord = autoclass("edu.stanford.nlp.ling.IndexedWord")
Annotation = autoclass("edu.stanford.nlp.pipeline.Annotation")
SemanticGraph = autoclass("edu.stanford.nlp.semgraph.SemanticGraph")

SemanticGraphCoreAnnotations = autoclass("edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations")
SemanticGraphCoreAnnotations.CollapsedCCProcessedDependenciesAnnotation = autoclass("edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations$CollapsedCCProcessedDependenciesAnnotation")

SemanticGraphEdge = autoclass("edu.stanford.nlp.semgraph.SemanticGraphEdge")
CoreMap = autoclass("edu.stanford.nlp.util.CoreMap")



props = Properties()
props.setProperty("annotators","tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref")

pipeline = StanfordCoreNLP(props)
doc = Annotation(mytext)

pipeline.annotate(doc)

annotations = doc.get(CoreAnnotations.SentencesAnnotation).get(0)

for i in range(annotations.get(CoreAnnotations.TokensAnnotation).size()):
    corelabel = annotations.get(CoreAnnotations.TokensAnnotation).get(i)
    print corelabel.get(CoreAnnotations.TextAnnotation)
    print corelabel.get(CoreAnnotations.NamedEntityTagAnnotation)



depgraph = annotations.get(SemanticGraphCoreAnnotations.CollapsedCCProcessedDependenciesAnnotation)


