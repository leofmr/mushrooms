from .tree_node import TreeNode

def parse_rules(text: str) -> list:
    """Parsea o string da árvore de decisão gerada pela DecidionTreeClassifation
    Parsea cada nódulo da árvore de decisão, transformando-a em uma lista de nódulos que compoêm uma regra.
    Com isso obtemos uma lista de regras, onde cada regra é uma lista de nódulos que
    começa um nódulo raiz e termina em um nódulo de folha.
    
    Cada nódulo é um objeto da classe TreeNode

    Args:
        text (str): representação textual da árvore de decisão 

    Returns:
        list: lista de regras (lista de nódulos)
    """
        
    node_list = text.strip().split("\n")
    
    rule_list = list()
    
    past_depth = 0
    present_rule = []
    
    for node_text in node_list:
        node = TreeNode(node_text)
        if node.depth > past_depth:
            present_rule.append(node)
        else:
            rule_list.append(present_rule)
            present_rule = present_rule[:node.depth-1]
        
        past_depth = node.depth
    
    return rule_list


def extract_dictionary_rule(branch: list) -> tuple(dict, str):
    """Separa uma regra (ramo) de uma árvore de decisão em um dicionário que representa as condições
    e um string que representa a predição (resultado) do ramo.
    O dicionário segue uma estrutura aninhada, onde no primeiro nível temos a variável, no segundo nível
    a relação lógica, podendo ser True para "igual" e False para "diferente". O último nível é uma lista com
    os atributos (categorias da variável) para qual a variável apresenta a relação. 

    Args:
        branch (list): lista de nódulos com uma origem (raiz) e fim (folha) de uma árvore de decisão

    Returns:
        dict, str: [description]
    """    
    prediction = None
    conditions_dict = dict()
    
    for node in branch:
        if node.is_leaf:
            prediction = node.prediction
        else:
            if node.variable not in conditions_dict:
                conditions_dict[node.variable] = dict()

            if node.is_equal not in conditions_dict[node.variable]:
                conditions_dict[node.variable][node.is_equal] = [node.category]
            else:
                conditions_dict[node.variable][node.is_equal].append(node.category)
    
    return conditions_dict, prediction


def gen_text(conditions_dict: dict, prediction: str) -> str:
    """Transforma o dicionário e a predição em um texto que expressa discursivamente
    a regra. Sendo que, por uma relação lógica, substitui as regras de ser diferentes
    para uma mesma variável referente a categorias distintas. 

    Args:
        conditions_dict (dict): dicionário com a estrutura das condições da regra
        prediction (str): texto com a previsão da regra

    Returns:
        str: texto que expressa discursivamente a regra.
    """    
    conditions_text_list = list()
    for var in conditions_dict.keys():
        selected_condition = True in conditions_dict[var].keys()
        relation_text = "equal to" if selected_condition == True else "not equal to"
        categories = " and ".join(conditions_dict[var][selected_condition])
        txt = " ".join([var, relation_text, categories])
        conditions_text_list.append(txt)
    
    return "If " + ", and ".join(conditions_text_list) + " then " + prediction