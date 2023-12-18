import json
import os
from pathlib import Path

import pytest
import requests
from dirty_equals import HasLen, HasAttributes, IsList, IsPartialDict
from pymultirole_plugins.v1.schema import Document, DocumentList, Sentence

from pyprocessors_openai_completion.openai_completion import (
    OpenAICompletionProcessor,
    OpenAICompletionParameters,
    OpenAIModel,
    flatten_document, OpenAIFunction, AzureOpenAICompletionProcessor,
    DeepInfraOpenAICompletionProcessor, AzureOpenAICompletionParameters,
    AZURE_CHAT_GPT_MODEL_ENUM, CHAT_GPT_MODEL_ENUM, DeepInfraOpenAICompletionParameters
)


def test_openai_completion_basic():
    model = OpenAICompletionProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == OpenAICompletionParameters

    model = AzureOpenAICompletionProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == AzureOpenAICompletionParameters

    model = DeepInfraOpenAICompletionProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == DeepInfraOpenAICompletionParameters


def test_flatten_doc():
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/complexdoc.json",
    )
    with source.open("r") as fin:
        jdoc = json.load(fin)
        doc = Document(**jdoc)
        flatten = flatten_document(doc)
        assert flatten == IsPartialDict(
            text=doc.text,
            title=doc.title,
            metadata_foo=doc.metadata["foo"],
            altTexts_0_name=doc.altTexts[0].name,
        )


JINJA_PROMPTS = {
    "preserve_entities": """Generates several variants of the following context while preserving the given named entities. Each named entity must be between square brackets using the notation [label:entity].
    Context: {{ doc.text }}
    {%- set entities=[] -%}
    {%- for a in doc.annotations -%}
      {%- do entities.append('[' + a.label + ':' + a.text + ']') -%}
    {%- endfor %}
    Given named entities using the notation [label:entity]: {{ entities|join(', ') }}
    Output language: {{ doc.metadata['language'] }}
    Output format: bullet list""",
    "substitute_entities": """Generates several variants of the following context while substituting the given named entities by semantically similar named entities with the same label, for each variant insert the new named entities between square brackets using the notation [label:entity].
    Context: {{ doc.text }}
    {%- set entities=[] -%}
    {%- for a in doc.annotations -%}
      {%- do entities.append('[' + a.label + ':' + a.text + ']') -%}
    {%- endfor %}
    Given named entities using the notation [label:entity]: {{ entities|join(', ') }}
    Output language: {{ doc.metadata['language'] }}
    Output format: bullet list""",
}


# @pytest.mark.skip(reason="Not a test")
@pytest.mark.skip(reason="Not a test")
@pytest.mark.parametrize("typed_prompt", [p for p in JINJA_PROMPTS.items()])
def test_jinja_doc(typed_prompt):
    type = typed_prompt[0]
    prompt = typed_prompt[1]
    parameters = OpenAICompletionParameters(
        max_tokens=3000,
        completion_altText=type,
        prompt=prompt,
    )
    processor = OpenAICompletionProcessor()
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/jinjadocs.json",
    )
    with source.open("r") as fin:
        jdocs = json.load(fin)
        docs = [Document(**jdoc) for jdoc in jdocs]
        docs = processor.process(docs, parameters)
        assert docs == HasLen(6)
        sum_file = testdir / f"data/jinjadocs_{type}.json"
        dl = DocumentList(__root__=docs)
        with sum_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
    # noqa: E501


def chunks(seq, size=1000):  # noqa
    return (seq[pos: pos + size] for pos in range(0, len(seq), size))


@pytest.mark.skip(reason="Not a test")
def test_semeval_docs():
    start_at = 32
    parameters = OpenAICompletionParameters(
        max_tokens=3000,
    )
    processor = OpenAICompletionProcessor()
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/semeval_fa_da.json",
    )
    with source.open("r") as fin:
        jdocs = json.load(fin)
        for i, chunk in enumerate(chunks(jdocs, 10)):
            if i >= start_at:
                docs = [Document(**jdoc) for jdoc in chunk]
                for type, prompt in JINJA_PROMPTS.items():
                    parameters.prompt = prompt
                    parameters.completion_altText = type
                    docs = processor.process(docs, parameters)
                    # assert docs == HasLen(6)
                    sum_file = testdir / f"data/semeval_fa_da_{type}_{i}.json"
                    dl = DocumentList(__root__=docs)
                    with sum_file.open("w") as fout:
                        print(
                            dl.json(exclude_none=True, exclude_unset=True, indent=2),
                            file=fout,
                        )


@pytest.mark.skip(reason="Not a test")
@pytest.mark.parametrize("model", [m for m in CHAT_GPT_MODEL_ENUM])
def test_openai_prompt(model):
    parameters = OpenAICompletionParameters(
        model=model, max_tokens=120, completion_altText="completion"
    )
    processor = OpenAICompletionProcessor()
    docs_with_prompts = [
        (
            Document(
                identifier="1",
                text="séisme de magnitude 7,8 a frappé la Turquie",
                metadata={"language": "fr"},
            ),
            "Peux tu écrire un article de presse concernant: $text",
        ),
        (
            Document(
                identifier="2",
                text="j'habite dans une maison",
                metadata={"language": "fr"},
            ),
            "Peux tu me donner des phrases similaires à: $text",
        ),
        (
            Document(
                identifier="3",
                text="il est né le 21 janvier 2000",
                metadata={"language": "fr"},
            ),
            "Peux tu me donner des phrases similaires en changeant le format de date à: $text",
        ),
        (
            Document(
                identifier="4",
                text="""Un nuage de fumée juste après l’explosion, le 1er juin 2019.
                Une déflagration dans une importante usine d’explosifs du centre de la Russie a fait au moins 79 blessés samedi 1er juin.
                L’explosion a eu lieu dans l’usine Kristall à Dzerzhinsk, une ville située à environ 400 kilomètres à l’est de Moscou, dans la région de Nijni-Novgorod.
                « Il y a eu une explosion technique dans l’un des ateliers, suivie d’un incendie qui s’est propagé sur une centaine de mètres carrés », a expliqué un porte-parole des services d’urgence.
                Des images circulant sur les réseaux sociaux montraient un énorme nuage de fumée après l’explosion.
                Cinq bâtiments de l’usine et près de 180 bâtiments résidentiels ont été endommagés par l’explosion, selon les autorités municipales. Une enquête pour de potentielles violations des normes de sécurité a été ouverte.
                Fragments de shrapnel Les blessés ont été soignés après avoir été atteints par des fragments issus de l’explosion, a précisé une porte-parole des autorités sanitaires citée par Interfax.
                « Nous parlons de blessures par shrapnel d’une gravité moyenne et modérée », a-t-elle précisé.
                Selon des représentants de Kristall, cinq personnes travaillaient dans la zone où s’est produite l’explosion. Elles ont pu être évacuées en sécurité.
                Les pompiers locaux ont rapporté n’avoir aucune information sur des personnes qui se trouveraient encore dans l’usine.
                """,
                metadata={"language": "fr"},
            ),
            "Peux résumer dans un style journalistique le texte suivant: $text",
        ),
        (
            Document(
                identifier="5",
                text="Paris is the capital of France and Emmanuel Macron is the president of the French Republic.",
                metadata={"language": "en"},
            ),
            "Can you find the names of people, organizations and locations in the following text:\n\n $text",
        ),
    ]
    docs = []
    for doc, prompt in docs_with_prompts:
        parameters.prompt = prompt
        doc0 = processor.process([doc], parameters)[0]
        docs.append(doc0)
        assert doc0.altTexts == IsList(
            HasAttributes(name=parameters.completion_altText)
        )
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / f"en_{model.value}.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


# noqa: E501
@pytest.mark.skip(reason="Not a test")
@pytest.mark.parametrize("model", [m for m in CHAT_GPT_MODEL_ENUM])
def test_openai_text(model):
    parameters = OpenAICompletionParameters(
        model=model,
        max_tokens=120,
        best_of=3,
        n=3,
        completion_altText="completion",
    )
    processor = OpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Peux tu écrire un article de presse concernant: séisme de magnitude 7,8 a frappé la Turquie",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="Peux tu me donner des phrases similaires à: j'habite dans une maison",
            metadata={"language": "fr"},
        ),
    ]
    docs = processor.process(docs, parameters)
    assert docs == HasLen(2)
    for doc in docs:
        assert doc.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / f"fr_{model.value}.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


# noqa: E501
@pytest.mark.skip(reason="Not a test")
def test_q_and_a():
    prompt = """Répondre à la question en utilisant les segments suivants et en citant les références.
    Question: {{ doc.altTexts[0].text }}
    Segments: {{ doc.text }}"""

    parameters = OpenAICompletionParameters(
        max_tokens=2000,
        completion_altText=None,
        prompt=prompt,
    )
    processor = OpenAICompletionProcessor()
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/question_segments.json",
    )
    with source.open("r") as fin:
        jdoc = json.load(fin)
        docs = [Document(**jdoc)]
        docs = processor.process(docs, parameters)
        assert docs == HasLen(1)
        sum_file = testdir / "data/question_segments_answer.json"
        dl = DocumentList(__root__=docs)
        with sum_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
    # noqa: E501


@pytest.mark.skip(reason="Not a test")
def test_azure_endpoint():
    parameters = AzureOpenAICompletionParameters(
        model=AZURE_CHAT_GPT_MODEL_ENUM("gpt-4"),
        max_tokens=1000,
        best_of=3,
        n=3,
        completion_altText="completion",
    )
    processor = AzureOpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Peux tu écrire un article de presse concernant: séisme de magnitude 7,8 a frappé la Turquie",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="Peux tu me donner des phrases similaires à: j'habite dans une maison",
            metadata={"language": "fr"},
        ),
    ]
    docs = processor.process(docs, parameters)
    assert docs == HasLen(2)
    for doc in docs:
        assert doc.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / "fr_azure_gpt_4.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        fout.write(dl.json(exclude_none=True, exclude_unset=True, indent=2))


@pytest.mark.skip(reason="Not a test")
def test_deepinfra_endpoint():
    parameters = DeepInfraOpenAICompletionParameters(
        max_tokens=100,
        completion_altText="completion",
    )
    processor = DeepInfraOpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Peux tu écrire un article de presse concernant: séisme de magnitude 7,8 a frappé la Turquie",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="Peux tu me donner des phrases similaires à: j'habite dans une maison",
            metadata={"language": "fr"},
        ),
    ]
    docs = processor.process(docs, parameters)
    assert docs == HasLen(2)
    for doc in docs:
        assert doc.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / "fr_llama2.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        fout.write(dl.json(exclude_none=True, exclude_unset=True, indent=2))


@pytest.mark.skip(reason="Not a test")
def test_direct_deepinfra():
    PROMPT = """[INST]Answer the question in french using the given segments of a long document and making references of those segments ["SEGMENT"] with the segment number. 
Be short and precise as possible. If you don't know the answer, just say that you don't know. Don't try to make up an answer.
Question: Est-il prévu des congés rémunérés pour les femmes souffrant de douleurs menstruelles ?

SEGMENTS:
1. À l’heure où certaines entreprises ou même certaines collectivités prévoient des congés rémunérés pour les femmes souffrant de douleurs menstruelles importantes ou d’endométriose, une proposition de loi a été déposée au Sénat en ce sens le 18 avril 2023 par une sénatrice socialiste et plusieurs de ses collègues. Les femmes concernées pourraient faire l’objet d’un arrêt de travail ou encore télétravailler, sous certaines conditions. La proposition de loi prévoit aussi un congé payé pour les femmes (et leur conjoint) ayant subi une fausse couche.

2. La proposition de loi prévoit de créer un arrêt de travail indemnisé pour les femmes souffrant de dysménorrhée (règles douloureuses) ou d’endométriose (maladie gynécologique inflammatoire et chronique). Prescrit par un médecin ou une sage-femme, cet arrêt maladie autoriserait la salariée à interrompre son travail chaque fois qu’elle se trouverait dans l’incapacité physique de travailler, pour une durée ne pouvant excéder 2 jours par mois sur une période de 3 mois. Les IJSS, versées sans délai de carence, se calculeraient selon des règles dérogatoires favorables à la salariée.  Dans l’objectif d’éviter un arrêt de travail, la proposition de loi vise aussi à favoriser la possibilité de télétravail pour les femmes souffrant de règles douloureuses et invalidantes, via l'accord collectif ou la charte sur le télétravail lorsqu'il en existe un.    Enfin, le texte propose de créer sur justification, pour les femmes affectées par une interruption spontanée de grossesse, un congé rémunéré de 5 jours ouvrables. Le conjoint, concubin ou partenaire pacsé de la salariée aurait aussi droit à ce congé.    Reste à voir si cette 2e proposition de loi, déposée le 18 avril par une sénatrice socialiste et plusieurs de ses collègues, connaîtra un sort aussi favorable que la première.

3. Maternité, paternité, adoption, femmes enceintes dispensées de travail - L’employeur doit compléter une attestation de salaire lorsque le congé de maternité* débute (c. séc. soc. art. R. 331-5, renvoyant à c. séc. soc. art. R. 323-10).      Le même document est à compléter en cas de congé d’adoption*, de congé de paternité et d’accueil de l’enfant* ou, dans le cadre de la protection de la maternité, pour les femmes travaillant de nuit ou occupant des postes à risques dispensées de travail en raison d’une impossibilité de reclassement sur un poste de jour ou sans risques .      Il s’agit de la même attestation que celle prévue pour les arrêts maladie.

4. Grossesse pathologique liée au distilbène - Le distilbène (ou diéthylstilbestrol) prescrit il y a plusieurs années entraîne des grossesses pathologiques chez les femmes qui y ont été exposées in utero.      Les femmes chez lesquelles il est reconnu que la grossesse pathologique est liée à l’exposition in utero au distilbène bénéficient d’un congé de maternité à compter du premier jour de leur arrêt de travail (loi 2004-1370 du 20 décembre 2004, art. 32         ; décret 2006-773 du 30 juin 2006, JO 2 juillet).

5. Enfant né sans vie - L'indemnité journalière de maternité est allouée même si l'enfant n'est pas né vivant au terme de 22 semaines d'aménorrhée (c. séc. soc. art. R. 331-5). Pathologie liée au Distilbène - Bien que ce médicament ne soit plus prescrit, le Distilbène (ou diéthyltilbestrol) peut entraîner des grossesses pathologiques pour les femmes qui y ont été exposées in utero. Les femmes dont il est reconnu que la grossesse pathologique est liée à l’exposition in utero au Distilbène bénéficient d’un congé de maternité à compter du premier jour de leur arrêt de travail (loi 2004-1370 du 20 décembre 2004, art. 32, JO du 21). Ces femmes peuvent prétendre à l’IJSS de maternité dès le début de leur congé de maternité si elles remplissent les conditions d’ouverture du droit au congé légal de maternité (décret 2006-773 du 30 juin 2006, JO 2 juillet).

6. Possibilité de télétravailler pour les femmes souffrant de règles douloureuses Dans l’objectif d’éviter un arrêt de travail pour douleurs menstruelles, la proposition de loi vise à favoriser la possibilité de télétravail aux femmes souffrant de dysménorrhée (proposition de loi, art. 4).   À cet égard, l'accord collectif ou la charte sur le télétravail existant dans l’entreprise devrait préciser les modalités d’accès des salariées souffrant de règles douloureuses et invalidantes à une organisation en télétravail.    En toute logique, il ressort de l’exposé des motifs que cela ne viserait que les femmes dont l’activité professionnelle est compatible avec l’exercice du télétravail.      À noter : en dehors d’un accord ou d’une charte sur le télétravail, il est toujours possible à l’employeur et au salarié de convenir d’un recours au télétravail formalisé par tout moyen (c. trav. art. L. 1222-9).Une proposition de loi en faveur des femmes souffrant de douleurs menstruelles, d’endométriose, ou ayant subi une fausse couche
    [/INST]"""
    api_key = os.getenv("DEEPINFRA_OPENAI_API_KEY")
    deploy_infer_url = "https://api.deepinfra.com/v1/inference/meta-llama/Llama-2-70b-chat-hf"
    response = requests.post(deploy_infer_url, json={
        "input": PROMPT,
        "max_new_tokens": 4096,
        "temperature": 0.2
    },
                             headers={'Content-Type': "application/json",
                                      'Authorization': f"Bearer {api_key}"})
    if response.ok:
        result = response.json()
        texts = "\n".join([r['generated_text'] for r in result['results']])
        assert len(texts) > 0


# noqa: E501

@pytest.mark.skip(reason="Not a test")
def test_function_call_ner():
    candidate_labels = {
        'per': 'Personne',
        'loc': 'Lieu géographique',
        'org': 'Organisation',
    }

    prompt = """Your task is to extract all occurences of named entities of the given labels in the provided text segments.
    Each text segment is prefixed by an index number followed by a closing parenthesis like 1) and postfixed by ===.
    Your response should include all identified named entities, their corresponding segment index numers, labels, and the start and end offsets in their correponding segment for each occurrence.
    {%- set labels=[] -%}
    {%- for l in parameters.candidate_labels.values() -%}
      {%- do labels.append('"' + l + '"') -%}
    {%- endfor %}
    Labels: {{ labels|join(', ') }}
    Segments:
    {%- for seg in doc.sentences %}
      {{ loop.index0 }}) {{ doc.text[seg.start:seg.end] }}
      ===
    {%- endfor %}"""

    parameters = OpenAICompletionParameters(
        model=OpenAIModel.gpt_3_5_turbo_16k_0613,
        max_tokens=14000,
        completion_altText=None,
        prompt=prompt,
        function=OpenAIFunction.add_annotations,
        candidate_labels=candidate_labels
    )
    processor = OpenAICompletionProcessor()
    docs = [
        Document(
            identifier="2",
            text="Cinq choses à savoir sur Toutankhamon et son fabuleux trésor\n\nL'ouverture, il y a 100 ans, du tombeau du pharaon égyptien Toutankhamon, l'une des plus grandes découvertes archéologiques de tous les temps, reste nimbée de mystères.\n\n\nVoici cinq choses à savoir sur l'enfant-roi, ses énigmes et ses trésors:\n\n\n- Un trésor inviolé -\n\n\nEn novembre 1922, après six saisons de fouilles infructueuses, l'archéologue britannique Howard Carter, son équipe égyptienne et le riche mécène Lord Carnarvon découvrent une sépulture inviolée dans la Vallée des Rois, près de Louxor en Haute-Egypte.\n\n\nLe trésor funéraire, réparti dans les cinq pièces du tombeau, est intact, avec 4.500 objets (mobilier, bijoux, statuettes), dont bon nombre en or massif.\n\n\nLe tombeau du jeune pharaon, mort à 19 ans aux environ de 1324 avant Jésus-Christ, est le seul mausolée de l'Egypte antique à avoir livré un tel trésor.\n\n\nLes innombrables autres tombeaux de pharaons et notables mis au jour jusqu'alors avaient été pillés au fil des millénaires.\n\n\n- Cercueil en or massif -\n\n\nParmi les objets découverts: un lit en bois plaqué or orné d'une tête de lion, un char ou encore un poignard au manche d'or, forgé à partir du fer de météorites selon des chercheurs.\n\n\nLe spectaculaire sarcophage en quartzite rouge hébergeait trois cercueils emboîtés les uns dans les autres, dont le dernier (110 kg) en or massif abritait la momie de Toutankhamon.\n\n\nMais la pièce maîtresse du trésor, devenue l'un des objets égyptiens les plus reconnaissables au monde, est un masque funéraire en or de plus de 10 kg incrusté de lapis-lazuli et d'autres pierres semi-précieuses.\n\n\n- Un arbre généalogique énigmatique -\n\n\nDes tests ont permis d'établir que le père de Toutankhamon était le pharaon Akhenaton, qui a régné entre 1351 et 1334 avant Jésus-Christ.\n\n\nAkhenaton était l'époux de la légendaire reine Néfertiti.\n\n\nPour autant, celle-ci n'est pas la mère de Toutankhamon. La mère du jeune pharaon, dont la momie a été retrouvée, serait la soeur de son père. L'analyse génétique montre en effet une consanguinité entre les parents.\n\n\nToutankhamon aurait épousé sa demi-soeur, Ankhsenpaamon. Le mariage entre frère et soeur était commun dans l'Egypte des pharaons.\n\n\nLe couple n'a pas de descendance connue mais deux momies d'enfants mort-nés ont toutefois été découvertes dans la tombe du jeune roi.\n\n\n- Un règne troublé, une mort mystérieuse -\n\n\nC'est à neuf ans, vers 1333 avant Jésus-Christ, que Toutankhamon serait monté sur le trône de Haute et Basse Egypte, mais les âges et les dates varient d'un spécialiste à l'autre.\n\n\nLe pays sort alors d'une période troublée, marquée par la volonté d'Akhenaton d'instaurer une forme de monothéisme dédiée au dieu du soleil Aton.\n\n\nL'arrivée au pouvoir du jeune prince permet aux tenants du culte d'Amon de reprendre le dessus et de rétablir les divinités traditionnelles.\n\n\nPlusieurs théories ont circulé sur les causes de son décès: maladie, accident de char ou meurtre.\n\n\nEn 2010, des tests génétiques et des études radiologiques ont révélé que l'adolescent serait en fait mort de paludisme combiné à une affection osseuse. Le jeune roi boitait d'un pied en raison d'une nécrose osseuse et son système immunitaire était déficient.\n\n\n- Un trésor maudit ? -\n\n\nQuelques mois après la fabuleuse découverte, le mythe de la malédiction du pharaon, qui frapperait ceux qui ont ouvert le tombeau, prend corps lorsque Lord Carnavon meurt en avril 1923 de septicémie, après une coupure infectée.\n\n\nLa légende se nourrit aussi d'une série de décès, comme celui de Carter qui meurt d'un cancer en 1939 à l'âge de 64 ans sans avoir achevé la publication de son ouvrage sur la sépulture, alors qu'il avait consacré dix ans à répertorier le trésor.\n\n\nAgatha Christie s'inspirera de la malédiction de Toutankhamon pour une de ses célèbres nouvelles: \"L'aventure du tombeau égyptien\".\n\n\nbur-kd-ays/mw/sbh/roc",
            sentences=[
                Sentence(start=0,
                         end=230
                         ),
                Sentence(start=233,
                         end=582
                         ),
                Sentence(start=585,
                         end=738
                         ),
                Sentence(start=741,
                         end=893
                         ),
                Sentence(start=896,
                         end=1019
                         ),
                Sentence(start=1022,
                         end=1232
                         ),
                Sentence(start=1235,
                         end=1415
                         ),
                Sentence(start=1418,
                         end=1630
                         ),
                Sentence(start=1633,
                         end=1810
                         ),
                Sentence(start=1813,
                         end=1870
                         ),
                Sentence(start=1873,
                         end=1929
                         ),
                Sentence(start=1930,
                         end=2015
                         ),
                Sentence(start=2016,
                         end=2088
                         ),
                Sentence(start=2091,
                         end=2147
                         ),
                Sentence(start=2148,
                         end=2220
                         ),
                Sentence(start=2223,
                         end=2356
                         ),
                Sentence(start=2359,
                         end=2583
                         ),
                Sentence(start=2586,
                         end=2731
                         ),
                Sentence(start=2734,
                         end=2874
                         ),
                Sentence(start=2877,
                         end=2974
                         ),
                Sentence(start=2977,
                         end=3128
                         ),
                Sentence(start=3129,
                         end=3235
                         ),
                Sentence(start=3238,
                         end=3258
                         ),
                Sentence(start=3259,
                         end=3490
                         ),
                Sentence(start=3493,
                         end=3738
                         ),
                Sentence(start=3741,
                         end=3896
                         )
            ],
            metadata={"language": "fr"},
        ),
        Document(
            identifier="1",
            text="Emmanuel Macron est le président de la France et Elizabeth Borne est la première-ministre de la France",
            sentences=[
                Sentence(
                    start=0,
                    end=102
                ),
            ],
            metadata={"language": "fr"},
        ),
    ]
    docs = processor.process(docs, parameters)
    assert docs == HasLen(2)
    doc0 = docs[0]
    for a in doc0.annotations:
        assert a.text == doc0.text[a.start:a.end]


@pytest.fixture
def expected_en():
    return {
        "Sport": "The french team is going to win Euro 2021 football tournament",
        "Politics": "Who are you voting for in 2021?",
        "Science": "Coronavirus vaccine research are progressing",
    }


@pytest.mark.skip(reason="Not a test")
def test_function_call_cat(expected_en):
    candidate_labels = {
        'sport': 'Sport',
        'politics': 'Politics',
        'science': 'Science',
    }

    prompt = """You are an expert Text Classification system. Your task is to accept Text as input and provide a category for the text based on the predefined labels.
{%- set labels=[] -%}
{%- for l in parameters.candidate_labels.values() -%}
  {%- do labels.append('"' + l + '"') -%}
{%- endfor %}
Classify the text below to one of the following labels: {{ labels|join(', ') }}
The task is exclusive, so only choose one label from what I provided.
Text: {{doc.text}}
"""

    parameters = OpenAICompletionParameters(
        model=OpenAIModel.gpt_3_5_turbo,
        completion_altText=None,
        prompt=prompt,
        function=OpenAIFunction.add_exclusive_category,
        candidate_labels=candidate_labels
    )
    processor = OpenAICompletionProcessor()
    docs = [Document(text=t) for t in expected_en.values()]
    docs = processor.process(docs, parameters)
    for expected_label, doc in zip(expected_en.keys(), docs):
        assert doc.categories[0].label == expected_label


@pytest.mark.skip(reason="Not a test")
def test_cairninfo():
    prompt = """Refais la ponctuation du texte suivant en français. Ce texte comporte plusieurs interlocuteurs. Va à la ligne à chaque fois que l'interlocuteur change : $text"""

    parameters = DeepInfraOpenAICompletionParameters(
        model="mistralai/Mistral-7B-Instruct-v0.1",
        max_tokens=4000,
        completion_altText=None,
        prompt=prompt,
    )
    processor = DeepInfraOpenAICompletionProcessor()
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/test_cairninfo-document-CNRRENC_013.txt.json",
    )
    with source.open("r") as fin:
        jdoc = json.load(fin)
        doc = Document(**jdoc)
        seg0 = Document(text=doc.text[doc.sentences[0].start:doc.sentences[0].end])
        segs = processor.process([seg0], parameters)
        assert segs == HasLen(1)
        sum_file = testdir / "data/test_cairninfo-document-CNRRENC_013.seg0.json"
        dl = DocumentList(__root__=segs)
        with sum_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
    # noqa: E501


@pytest.mark.skip(reason="Not a test")
def test_resume_mixtral():
    text = """La puissance des Gafam
Les transformations économiques de l’espace médiatique contemporain
Nathalie Sonnac

La mutation numérique du monde se traduit par la combinaison de deux caractéristiques : la mise en réseaux et la mise en données. Elles sont au cœur des modèles d’organisation des plateformes numériques qui installent une nouvelle forme d’organisation de la production et des échanges, intègrent des logiques de marchés dématérialisés, ordonnent et orchestrent un large écosystème d’utilisateurs et de producteurs, notamment des contenus qu’elles éditorialisent elles-mêmes. Aux États-Unis, ce panorama est dominé par quatre firmes connues sous l’acronyme Gafam, pour Google (devenu Alphabet), Apple, Facebook (devenu Méta), Amazon et Microsoft. Surpuissantes économiquement et financièrement, ces plateformes numériques ont envahi notre espace informationnel et communicationnel. Elles ont investi en 2021 plus de cent milliards de dollars dans des films, séries, documentaires et droits sportifs contre six milliards, en cinq ans, en obligations d’investissement audiovisuels et cinématographiques par les groupes TF1, M6, Canal+ et France Télévisions.
En quelques années, les Gafam se sont imposés, déstabilisant les médias historiques, qui subissent en parallèle, depuis plusieurs années, une crise de confiance et une désaffection de leurs consommateurs, dans un univers numérique où les journalistes n’ont plus le monopole de la diffusion d’informations et ne peuvent plus exercer leur rôle de filtre : 71 % des 15-34 ans déclarent utiliser les réseaux sociaux pour s’informer, loin devant les JT, les flashs d’info ou encore la presse quotidienne, même en ligne. Le marché de l’information est en crise, pollué aussi par la circulation de fausses informations et de discours haineux, et évoluant dans un cadre législatif désuet : « La matrix politica, ensemble des lois et des règles qui régit l’espace de la communication dans lequel nous échangeons des informations, des idées, des opinions, est aujourd’hui corrompue. »
Pour comprendre l’économie des médias, des préalables indispensables doivent être posés. D’abord les deux injonctions contradictoires qui se posent à ces secteurs. La première suppose d’accepter – enfin ! – de considérer les médias comme des entreprises à part entière. Trop souvent, ils sont présentés comme des entreprises subventionnées, « danseuses » d’entrepreneurs milliardaires en recherche d’influence sur la sphère sociale et politique. Cependant, ils évoluent depuis toujours dans un écosystème marchand et concurrentiel. Le secteur de l’audiovisuel français pèse à lui seul plus de dix milliards d’euros pour plus de cent mille emplois et il est créateur de richesses et d’innovations. En même temps, les médias sont des entreprises entièrement à part. L’information n’étant ni une automobile ni un pot de yaourt, elle se trouve en danger lorsque le nombre de journalistes diminue, lorsque la liberté d’expression n’est pas garantie par un cadre réglementaire ou une autorité indépendante, ou encore lorsque le pluralisme des opinions et la diversité des canaux de diffusion sont insuffisants.
Ensuite, l’économie des médias se caractérise par une structure de coûts fixes importants, car l’information coûte cher à produire, à collecter, à traiter, à vérifier, alors même que le coût de reproduction est quasi nul. Dès lors, pour amortir ces coûts fixes et bénéficier d’économies d’échelle, les entreprises sont conduites à produire en grande quantité ; la taille de marché est alors une composante essentielle pour la viabilité de leur modèle. En outre, les médias présentent un certain nombre de caractéristiques économiques. Comme l’information est classée dans la catégorie des biens publics (non rivaux, non exclusifs), le marché est défaillant à la produire, justifiant de facto l’intervention de l’État sous forme d’aides à la presse ou de redevance. De surcroît, les médias revêtent un caractère d’intérêt général (bien sous-tutelle). L’information est également un bien d’expérience, on ne connaît sa valeur qu’une fois consommée (nobody knows), un caractère qui oblige les producteurs à multiplier les dépenses en marketing et en promotion et exacerbe la concurrence sur sa signalisation. Notons que dans la mesure où la capacité d’expérience des consommateurs est limitée dans le temps, une guerre d’attention va se jouer entre l’ensemble des producteurs d’information : médias, réseaux sociaux, agrégateurs, moteurs de recherche… pour nous accaparer.
Trois révolutions pour une métamorphose
Avec l’arrivée d’Internet, les médias ont changé de paradigme. Le numérique a modifié intrinsèquement les modalités de production, de consommation et de diffusion des produits culturels et médiatiques. Ces transformations se sont traduites par une triple révolution dont les effets se combinent.
D’abord, une révolution technologique. Le numérique offre de nouvelles modalités d’accès aux contenus – numérisation des signaux, amélioration des réseaux, généralisation d’équipements à des prix abordables, etc. Le numérique permet ainsi aux téléspectateurs de regarder des programmes audiovisuels en dehors de leur antenne râteau, ils accèdent gratuitement à vingt-six chaînes de la TNT, des centaines via le câble et le satellite, des milliers via la fibre et l’ADSL. Depuis plusieurs années, les chaînes traditionnelles ont étendu leur offre linéaire avec des programmes à la demande et accessibles en rattrapage (délinéarisation) grâce à une diffusion en streaming rendue possible par le biais d’Internet, via des fournisseurs d’accès à Internet (FAI) ou en accès ouvert (OTT, over the top). Les médias ont également enrichi leurs offres grâce à de nouveaux formats, comme les podcasts natifs qui ont bouleversé le monde de la radio.
Ensuite, une révolution économique. Le développement du numérique s’est accompagné d’un changement de structure des marchés avec une captation de la valeur par de nouveaux acteurs puissants, certains issus des groupes de télécoms (Orange, Altice/SFR, AT&T), des groupes spécialisés (Netflix, HBO Max, Amazon Prime Video, Disney+) et des plateformes numériques venues concurrencer directement les acteurs traditionnels, comme c’est le cas pour le marché de la musique dominé par Spotify et Deezer. La multiplication des opérateurs et des offres de services a conduit à une fragmentation des audiences poussant les médias à réaliser des économies d’échelle plus importantes, à trouver de nouveaux relais de croissance, à engager des mouvements de concentration, d’industrialisation et de convergence qui reconfigurent le paysage médiatique.
Enfin, une révolution d’usage. Philippe Lombardo et Loup Wolff notent la place croissante des pratiques culturelles numériques et celle prise par l’audiovisuel dans le quotidien des Français depuis une décennie. Plus d’un tiers d’entre eux écoutent de la musique en ligne, 44 % jouent à des jeux vidéo et les trois quarts des 15-24 ans regardent des vidéos en ligne. Les plus jeunes se singularisent, 12 % des Américains âgés de 18 à 29 ans utilisent la télévision comme moyen d’accéder à l’information contre 43 % des plus de 65 ans. En France, 1 % des jeunes achètent la presse quotidienne. Le numérique est une révolution, qui a permis au consommateur de devenir producteur, distributeur et prescripteur de contenus ; d’écouter sa musique en streaming, de regarder ses vidéos à n’importe quel moment grâce aux services de vidéo à la demande (SVOD) par abonnement et à la télévision en rattrapage, de consommer ses séries en continu (binge watching), obligeant les producteurs et diffuseurs à revoir l’ensemble de la chaîne de valeur de production des films et des séries.
La plongée dans le numérique a favorisé les phénomènes de concentration. Si l’on compare, on peut considérer l’économie des médias comme l’ancêtre de l’économie des plateformes numériques. Depuis Émile de Girardin en 1836, la publicité est présente dans leur modèle d’affaires, elle représente 100 % des revenus des télévisions et des radios commerciales et a pu représenter jusqu’à 80 % des recettes d’un périodique dans les années 1970. Les médias, considérés par les économistes industriels depuis les années 2000 comme des plateformes de marchés à deux versants (two-sided markets [4][4]Voir Jean-Charles Rochet et Jean Tirole, « Platform Competition…), s’adressent à deux catégories d’agents, les annonceurs et les consommateurs. Les interactions entre médias et consommateurs d’une part (sur le marché des médias) et entre médias et annonceurs d’autre part (sur le marché publicitaire) sont appelées « effets de réseaux croisés » (la valeur d’un réseau augmente avec le nombre d’utilisateurs) ; elles sont au cœur de leurs modèles d’affaires [5][5]Côté consommateurs, leur intérêt dépend du prix d’accès, de la…. Comme les médias, les Gafam sont des plateformes d’échanges plongées dans le numérique, où les effets de réseaux croisés sont amplifiés. Stimulée par le phénomène de masse critique, à partir d’un certain nombre d’abonnés, la dynamique d’adoption s’autoalimente et se renforce toute seule. Il n’est alors plus nécessaire de subventionner les utilisateurs pour les attirer (gratuité), ils ont plus d’utilité à être présents qu’à être exclus. Ce n’est plus l’espace de l’offre de la fonction de production qui va organiser le marché, mais la dynamique de la demande. Le caractère mondial de leurs effets de réseaux décuple leur efficacité et favorise l’émergence de très grands acteurs. C’est l’économie du winner takes all aux conséquences démocratiques dévastatrices. Nous y reviendrons. Les transferts d’audience vers le numérique ont été suivis par les annonceurs, qui sont les principaux financeurs des médias [6][6]Les annonceurs ont investi à hauteur de 25 % de leurs dépenses…. Ce marché est dominé par trois acteurs, Google, Apple et Facebook et a été rejoint récemment par Amazon. La monétisation de leurs services gratuits représente 80 % du chiffre d’affaires de Google et 95 % de celui de Facebook. Les Gafam siphonnent ainsi les recettes publicitaires des médias et remettent en cause leur modèle économique.
À cette restructuration économique, s’ajoute une transformation organisationnelle qui se fait ici aussi au détriment des médias. Le nouvel écosystème publicitaire numérique est devenu complexe et fortement intermédié. Les relations de gré à gré entre annonceurs, agences et régies ont été abandonnées au milieu des années 1990 dans un contexte d’innovation technologique permettant le micro-ciblage, la collecte massive de données personnelles et le foisonnement d’espaces disponibles. La vente d’espaces publicitaires s’est automatisée avec des opérations d’allocation réalisées quasiment en temps réel (real time bidding) et des intermédiaires techniques sont progressivement devenus des points de passage obligés (gatekeepers). Google se situe à tous les étages de cette chaîne de valeur, et privilégie ses propres solutions au détriment de celles de ses concurrents.
De nouveaux modèles de recommandation, fondés sur les big data, les algorithmes et l’intelligence artificielle, ont également émergé. Le succès d’une plateforme tient en sa capacité à structurer ses utilisateurs en communautés, à leur proposer des services et des outils qui facilitent leurs interactions sociales virtuelles via des systèmes de certification et de recommandation. Parce que la puissance du modèle d’affaires des plateformes numériques repose sur leur capacité à générer des effets de réseaux et à jouer d’effets de taille permis par la gratuité d’accès aux services, la collecte massive de données (big data) et leur exploitation par des algorithmes et l’intelligence artificielle sous-tendent leurs modèles. Pétrole du xxie siècle, les données sont la nouvelle matière première à extraire. Elles représentent, comme le dit Pierre Louette, « d’immenses réservoirs, de segmentation, de prédictibilité qui servent toutes les opportunités de recommandation, de proposition ciblée et de monétisation [7][7]Pierre Louette, Des géants et des hommes. Pour en finir avec… ». Dans le domaine de l’information, Facebook propose un service d’actualités qui transmet à l’utilisateur des nouvelles récentes en s’appuyant sur des algorithmes dits de classement qui hiérarchisent les contenus s’affichant dans son fil d’actualités. Ces processus se basent sur nos consommations et celles de nos amis, sur nos engagements, nos partages et nos liens. Ainsi, la qualité des profils publicitaires présentée par la plateforme à ses annonceurs est proportionnelle à notre temps passé et à nos interactions en ligne. Ainsi, la sociologue Shoshana Zuboff écrit : « Les Big Tech nous connaissent mieux que nous-mêmes car ils peuvent prédire nos émotions, nos préférences politiques, nos orientations sexuelles. »
Reconfiguration du paysage
Dans ce marché international à forte pression concurrentielle, chacun tente de bénéficier d’effets de taille et de larges capacités d’investissement pour acquérir des contenus qui retiendront l’attention des consommateurs. Netflix a investi 17 milliards de dollars dans les contenus en 2020, Amazon Prime Video a racheté en mai 2021 pour 8,7 milliards de dollars les célèbres studios de la Metro-Goldwyn-Mayer (MGM), dont le catalogue détient plus de 4 000 films (James Bond, Rocky) et près de 17 000 heures de séries. L’offre de services de SVOD est devenue le cœur de métier des Gafam.
Depuis plusieurs mois, on a pu observer des mouvements de concentration aux États-Unis entre opérateurs de télécom et groupes de médias : AT&T a fait l’acquisition d’un bouquet télé satellitaire, Vérizon a acquis le portail AOL et ComCast a acheté NBC Universal. Plus récemment, des mouvements ont lieu au sein des filières de l’audiovisuel et du cinéma : Warner Bros/Discovery, ComCast/Universal Pictures, Disney/Century Fox, ViaComCBS/Paramount. En Europe, on observe des mouvements semblables, avec notamment la réorganisation du groupe Bertelsmann et le rachat de Simon & Schuster, numéro 2 de l’édition, pour 2,2 milliards de dollars ; en France, les fusions des groupes Vivendi-Editis et Lagardère-Publishing, et celles des groupes TF1 et M6 sont en cours.
Attaquées sur tous les fronts – fragmentation des audiences, chute des recettes publicitaires, baisse du nombre d’abonnés –, toutes les chaînes (publiques, privées et commerciales) tentent de faire front, en nouant des partenariats entre acteurs historiques (TF1, M6 et France Télévisions ont créé Salto) ; en mutualisant des investissements ou en cofinançant des projets. Au niveau européen, depuis 2018, les trois groupes publics audiovisuels – la ZDF, la RAI et France Télévisions ont créé l’Alliance, avec des projets de séries communes. Leonardo a pu bénéficier d’un budget de 3 millions d’euros par épisode, aucun groupe individuellement n’aurait eu les moyens de débourser un tel montant. Des partenariats sont également passés avec des plateformes, comme le groupe TF1 en 2019 avec Netflix pour coproduire la série Le Bazar de la charité. À l’exception de Sony Pictures, tous les studios américains sont aujourd’hui liés à une plateforme : Warner Bros diffuse ses propres films sur le service de streaming HBO et la Walt Disney Company propose certains de ses films sur son service de SVOD, Disney+.
La puissance de ces acteurs se mesure à leur capacité à investir dans les contenus, mais les milliards de dollars dépensés ont pour effet d’inonder le marché mondial de leurs productions, asséchant petit à petit les marchés locaux et poussant à une inflation généralisée des droits. Par leur surpuissance, elles imposent de nouvelles pratiques commerciales, raréfient les mécanismes d’accords avec les chaînes et nouent des accords de production (output deals) plus longs entre elles, allant jusqu’à l’acquisition de studios. Cette guerre du streaming se joue également sur l’acquisition de catalogues en exclusivité, obligeant le consommateur à démultiplier ses abonnements pour y accéder. Une stratégie qui s’avère coûteuse pour lui. Cette pratique est de plus en plus dénoncée pour les retransmissions sportives où les consommateurs doivent payer plusieurs abonnements pour suivre un événement intégralement.
La distribution de contenus, en Internet ouvert ou via un fournisseur d’accès à Internet, est également un élément clé de leur stratégie. Pour être accessible par le plus grand nombre, Netflix a par exemple fait le choix d’une distribution en partenariat avec des distributeurs locaux, ce qu’il a fait en France avec le groupe Canal+. L’avantage des plateformes réside dans leur modèle économique natif du numérique qui leur permet un accès direct à leurs abonnés : collecte massive des données des utilisateurs, interactions avec la plateforme, algorithmes de filtrage collaboratif… leur permettent d’analyser les habitudes de chacun et d’avoir une vision très précise de ses goûts. Ainsi, les programmes diffusés sont en lien avec les attentes et les plateformes peuvent ainsi renforcer leurs offres de catalogue.
Cette reconfiguration du paysage médiatique n’est pas qu’économique. Les Gafam sont un oligopole concentré horizontalement et verticalement, ils exercent leur pouvoir sur les fournisseurs de contenus et les consommateurs dans leur politique de modération. Mais par leur puissance, ils ont également la capacité à fixer eux-mêmes les règles du jeu sociétal, voire démocratique : quid de la liberté d’expression, du pluralisme et de l’honnêteté de l’information, de la protection des plus faibles ?
Des conséquences désastreuses sur le plan démocratique
Les dangers démocratiques que représente la présence de ces plateformes numériques dans le champ informationnel sont nombreux. Nous en relèverons ici trois.
D’abord, les Gafam diminuent le pluralisme et augmentent la concentration des médias. En siphonnant 85 % des recettes publicitaires en ligne, grand nombre d’entreprises médiatiques se voient dans l’obligation de fermer leurs portes, de se regrouper ou de réduire drastiquement le nombre de leurs journalistes, altérant ainsi la qualité des titres, au risque d’être moins attractifs auprès des consommateurs et donc des annonceurs. À cela s’ajoute un phénomène que l’on constate : l’émergence des pratiques numériques se corrèle au déclin du journalisme local. Le rapport du comité Stigler (2019) relève qu’au Royaume-Uni, le déploiement d’Internet a remplacé radios et journaux et s’est accompagné d’une diminution du taux de participation aux élections. Cet effet serait plus prononcé chez les plus jeunes et les moins instruits. Aux États-Unis, l’arrivée de la télévision s’est traduite par une baisse de la participation électorale et de la connaissance politique. Les médias traditionnels qui participent à la fabrique de l’opinion se voient évincés économiquement, mais leur déclin porte préjudice au bon fonctionnement démocratique. Paradoxalement, nous sommes projetés dans un espace informationnel plus large, mais moins démocratique.
Une autre conséquence désastreuse sur le plan démocratique est la déstabilisation possible, voire l’inversion des scrutins lors d’élections. Tel fut le cas dénoncé par le lanceur d’alerte Christopher Wylie de la société d’influence Cambridge Analytica, qui a siphonné des millions de profils d’utilisateurs de Facebook à leur insu pendant des années. Par sa connaissance affinée de chacun et une exploration systématique des données (data mining), elle a pu envoyer des centaines de milliers de messages personnalisés, sans que les individus concernés n’aient préalablement explicité leurs préférences. In fine, ces procédures peuvent déposséder les choix des individus et réduire leur libre arbitre.
Enfin, une dernière illustration du danger démocratique nous est donnée par Giuliano da Empoli. Il s’interroge sur les origines de la création du Mouvement 5 étoiles en Italie, sur les élections de Donald Trump aux États-Unis et de Jair Bolsonaro au Brésil, et sur le vote du Brexit au Royaume-Uni. Comment un parti politique a-t-il réussi à « transformer le plomb des data en or électoral » ? Deux hommes ont cofondé le Mouvement 5 étoiles : le comique Beppe Grillo et un expert en marketing digital, Gianroberto Casaleggio. Leur objectif : identifier les thèmes les plus fédérateurs qui remontent du blog de Beppe Grillo, dans un processus d’interaction constante, où le profil des personnes liées au mouvement permettait de savoir où elles vivaient, pour qui elles votaient, ce qu’elles aimaient, qui elles étaient. Les données sont devenues l’enjeu principal d’un match politique colossal, où Internet coïncide à un instrument de contrôle.
L’indispensable rôle de la régulation
Ce changement de paradigme pour les médias plongés dans le numérique suppose un dépassement des cadres nationaux pour leur régulation. L’échelle européenne doit être le niveau de référence pour fixer les fondements d’un espace numérique régional, uni autour de principes essentiels de respect des personnes et de promotion de la diversité culturelle.
Des avancées récentes ont eu lieu. D’abord fin 2021, avec la transposition de la directive des services de médias audiovisuels (directive SMA) dans la loi de 1986, qui a permis d’étendre le pouvoir des autorités de régulation de l’audiovisuel (en France le CSA, devenu Arcom) aux réseaux sociaux et aux plateformes de partage de vidéo. Celles-ci sont désormais contraintes de participer au financement de la création, réduisant un peu l’inégalité de traitement avec les chaînes. Deux nouveaux règlements européens – le Digital Service Act (DSA) et le Digital Market Act (DMA) – sont également en cours de révision avec pour objectif une responsabilisation des plateformes dans la lutte contre la diffusion de contenus haineux et une plus grande transparence sur la modération des contenus.
C’est également dans ce contexte de nouvel espace civique numérisé, où les désinformations circulent à la vitesse grand V et où le contrôle des contenus demeure le privilège exclusif des Big Tech, que la problématique de la concentration des médias doit être repensée. Compte tenu du caractère public et d’intérêt général de l’information, au danger classique du pouvoir économique concentré entre les mains de quelques-uns s’ajoute celui de l’influence politique. Les firmes médiatiques, comme les plateformes numériques, doivent pouvoir être compétitives, réaliser des économies d’échelle, bénéficier de synergies, acquérir des droits. Or les autorités de régulation, en application des lois de 1984 (pour la presse) et de 1986 (pour l’audiovisuel) ont tenté, au-delà de la lutte traditionnelle d’abus de position dominante, d’empêcher la création de grands groupes, essayant de conjuguer les injonctions contradictoires. Mais les effets de réseaux générés, issus directement de leur modèle de marché à deux versants (non pris en compte par les autorités), conduisent mécaniquement à une concentration du marché, sans pour autant que le pluralisme se perde. C’est l’une des complexités d’analyse du secteur, qui doit conjuguer, nous l’avons vu en liminaire, logique économique et impératif de préservation du pluralisme des courants de pensées dont le respect, rappelons-le, est consubstantiel au débat démocratique. Plusieurs pistes sont ouvertes : une redéfinition d’un nouveau marché pertinent de l’information ; l’abandon de l’analyse en silo prenant en compte les nouveaux usages ; la création de fondations à but non lucratif, comme Mediapart a pu le faire, ou encore la piste ouverte par l’universitaire Andrea Prat, qui propose le calcul d’un indice de puissance médiatique global, fondé sur la part d’attention.
Enfin, les pouvoirs publics doivent trouver une régulation économique de l’actif stratégique du numérique, les données. Leur valeur réside à la fois dans leur usage, leur traitement et leur circulation. C’est l’accès direct aux données générales ou personnelles des utilisateurs qui est, pour celui qui les possède ou les contrôle, une source de profit assuré. Comment garantir des méthodes de collecte et des traitements transparents et loyaux ? Comment assurer la finalité de leur utilisation ? Comment être certain qu’il n’y ait pas un détournement de leur usage ? Des conditions d’accès équitables et loyales aux données de consommation des programmes doivent être assurées, ainsi que le partage des données et le partage de la valeur de la donnée entre FAI et éditeurs de chaînes. L’Europe, depuis de nombreux mois, s’est engagée dans une nouvelle forme de régulation. Elle s’est dotée d’un nouveau cadre, sorte de « tiers modèle » qui n’est ni le laisser-faire états-unien ni le contrôle d’État des contenus chinois. Un modèle qui repose sur l’obligation de moyens, de transparence et de coopération des opérateurs. Cela représente un véritable défi pour les autorités nationales de régulation de l’audiovisuel, un défi indispensable à relever pour sauvegarder nos démocraties aujourd’hui mises en danger.
"""
    prompt = """Résumez le texte ci-dessous en langue française et en étant aussi bref et précis que possible.
Texte à résumer : $text"""

    parameters = DeepInfraOpenAICompletionParameters(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        max_tokens=4000,
        completion_altText=None,
        prompt=prompt,
    )
    processor = DeepInfraOpenAICompletionProcessor()

    processor.process([Document(text=text)], parameters=parameters)
    # noqa: E501
