import sys


number_ne_types = ['NUMBER','MONEY','PERCENT']
number_ne_types_for_match = ['NUMBER','MONEY','PERCENT','DATE']

months = ["January","February","March","April","May","June","July","August","September","October","November","December"]

def is_num(s):
    return num(s) is not None

def num(s):
    if type(s) == BigDecimal:
        s = Double.valueOf(s.toString())

    if type(s) == int:
        return s

    if type(s) == float:
        return s

    if s in months:
        return months.index(s)+1

    try:
        return int(s.replace(",",""))
    except ValueError:
        try:
            return float(s.replace(",",""))
        except:
            return None

def strnum(s):
    if type(s) == BigDecimal:
        s = str(Double.valueOf(s.toString()))

    try:
        return str(int(s.replace(",","")))
    except ValueError:
        return str(float(s.replace(",","")))


def nps_from_tree(tree):
    np_trees = find_np_subtrees(tree)

    chunks = []

    for tree in np_trees:
        chunks.append(flatten_tree(tree))

    return chunks


def flatten_tree(tree):
    words = []

    if type(tree) == str:
        return tree

    if tree.isLeaf():
        return tree.nodeString()


    for i in range(tree.numChildren()):
        subtree = tree.getChild(i)
        words.append(flatten_tree(subtree))

    return " ".join(words)


def find_np_subtrees(tree):
    np_trees = []
    for i in range(tree.numChildren()):
        subtree = tree.getChild(i)

        if subtree.label().value() == "NP":
            found = find_np_subtrees(subtree)
            if len(found) == 0:
                np_trees.append(subtree)
            else:
                np_trees.extend(found)
        elif not subtree.isLeaf():
            np_trees.extend(nps_from_tree(subtree))

    return np_trees




def chunk(annotations,option):
    last_ne = []
    chunked_nes = []
    for i in range(annotations.get(CoreAnnotations.TokensAnnotation).size()):
        if(i>0):
            if(option[i-1]):
                if(option[i]):
                    last_ne.append(annotations.get(CoreAnnotations.TokensAnnotation).get(i).get(CoreAnnotations.TextAnnotation))

                else:
                    if (len(last_ne)>0):
                        chunked_nes.append(" ".join(last_ne))
                        last_ne = []
            else:
                if(option[i]):
                    last_ne.append(annotations.get(CoreAnnotations.TokensAnnotation).get(i).get(CoreAnnotations.TextAnnotation))

        else:
            if (option[i]):
                last_ne.append(annotations.get(CoreAnnotations.TokensAnnotation).get(i).get(CoreAnnotations.TextAnnotation))


    if (len(last_ne) > 0):
        chunked_nes.append(" ".join(last_ne))

    return chunked_nes


def chunk_num(annotations,option):
    last_ne = []
    chunked_nes = []
    for i in range(annotations.get(CoreAnnotations.TokensAnnotation).size()):
        if(i>0):
            if(option[i-1]):
                if(option[i]):
                    v=annotations.get(CoreAnnotations.TokensAnnotation).get(i).get(CoreAnnotations.NumericCompositeValueAnnotation)
                    if v is not None:
                        last_ne.append(strnum(v))

                else:
                    if (len(last_ne)>0):
                        chunked_nes.append(" ".join(last_ne))
                        last_ne = []
            else:
                if(option[i]):
                    v = annotations.get(CoreAnnotations.TokensAnnotation).get(i).get(
                        CoreAnnotations.NumericCompositeValueAnnotation)
                    if v is not None:
                        last_ne.append(strnum(v))
        else:
            if (option[i]):
                v = annotations.get(CoreAnnotations.TokensAnnotation).get(i).get(
                    CoreAnnotations.NumericCompositeValueAnnotation)
                if v is not None:
                    last_ne.append(strnum(v))

    if (len(last_ne) > 0):
        chunked_nes.append(" ".join(last_ne))

    return chunked_nes




def compound(dep_graph,annotations,tagged):
    compound_nes = tagged

    changed = 1
    while changed > 0:
        changed = 0

        for i in range(annotations.get(CoreAnnotations.TokensAnnotation).size()):
            token = annotations.get(CoreAnnotations.TokensAnnotation).get(i)

            iterator = dep_graph.edgeIterable().iterator()

            while(iterator.hasNext()):
                edge = iterator.next()


                if(edge.getGovernor().index() == edge.getDependent().index()):
                    continue

                if(edge.getGovernor().index()-1 == i and compound_nes[edge.getGovernor().index()-1]):
                    if(edge.getRelation().getShortName() in ['compound','amod','nummod']):
                        if not compound_nes[edge.getDependent().index()-1] == compound_nes[edge.getGovernor().index()-1]:
                            changed +=1

                        compound_nes[edge.getDependent().index()-1] = compound_nes[edge.getGovernor().index()-1]

                elif (edge.getGovernor().index()-1 == i and compound_nes[edge.getDependent().index()-1]):
                    if(edge.getRelation().getShortName() in ['compound','amod','nummod']):
                        if not compound_nes[edge.getGovernor().index()-1] == compound_nes[edge.getDependent().index()-1]:
                            changed +=1

                        compound_nes[edge.getGovernor().index()-1] = compound_nes[edge.getDependent().index()-1]


    return compound_nes



from jnius import autoclass


Properties = autoclass("java.util.Properties")
StanfordCoreNLP = autoclass("edu.stanford.nlp.pipeline.StanfordCoreNLP")
CoreAnnotations = autoclass("edu.stanford.nlp.ling.CoreAnnotations")

CoreAnnotations.TokensAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$TokensAnnotation")
CoreAnnotations.SentencesAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$SentencesAnnotation")
CoreAnnotations.TextAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$TextAnnotation")
CoreAnnotations.NamedEntityTagAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$NamedEntityTagAnnotation")
CoreAnnotations.PartOfSpeechAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$PartOfSpeechAnnotation")
CoreAnnotations.LineNumberAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$LineNumberAnnotation")

CoreAnnotations.NumericValueAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$NumericValueAnnotation")
CoreAnnotations.NumericTypeAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$NumericTypeAnnotation")
CoreAnnotations.NumericCompositeValueAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$NumericCompositeValueAnnotation")

CorefChainAnnotation = autoclass("edu.stanford.nlp.hcoref.CorefCoreAnnotations$CorefChainAnnotation")

Double = autoclass("java.lang.Double")
BigDecimal = autoclass("java.math.BigDecimal")

CoreLabel = autoclass("edu.stanford.nlp.ling.CoreLabel")
IndexedWord = autoclass("edu.stanford.nlp.ling.IndexedWord")
Annotation = autoclass("edu.stanford.nlp.pipeline.Annotation")
SemanticGraph = autoclass("edu.stanford.nlp.semgraph.SemanticGraph")

SemanticGraphCoreAnnotations = autoclass("edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations")
SemanticGraphCoreAnnotations.CollapsedCCProcessedDependenciesAnnotation = autoclass("edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations$CollapsedCCProcessedDependenciesAnnotation")


Integer = autoclass("java.lang.Integer")

SemanticGraphEdge = autoclass("edu.stanford.nlp.semgraph.SemanticGraphEdge")
CoreMap = autoclass("edu.stanford.nlp.util.CoreMap")

NumberNormalizer = autoclass("edu.stanford.nlp.ie.NumberNormalizer")




TreeCoreAnnotations = autoclass("edu.stanford.nlp.trees.TreeCoreAnnotations")
TreeCoreAnnotations.TreeAnnotation = autoclass("edu.stanford.nlp.trees.TreeCoreAnnotations$TreeAnnotation")


class SharedPipeline:
    pipeline = None

    def __init__(self):
        if self.pipeline is None:
            props = Properties()
            props.setProperty("annotators", "tokenize,ssplit,pos,lemma,ner,parse,depparse")
            props.setProperty("parse.maxlen","100")
            pipeline = StanfordCoreNLP(props)
            self.pipeline = pipeline

    def getInstance(self):
        return self.pipeline


class SharedNERPipeline:
    pipeline = None

    def __init__(self):
        if self.pipeline is None:
            props = Properties()
            props.setProperty("annotators", "tokenize,ssplit,pos,lemma,ner")
            props.setProperty("parse.maxlen", "100")

            pipeline = StanfordCoreNLP(props)
            self.pipeline = pipeline

    def getInstance(self):
        return self.pipeline