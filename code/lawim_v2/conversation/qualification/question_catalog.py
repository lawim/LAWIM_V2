from __future__ import annotations

QUESTION_CATALOG: dict[str, dict[str, str]] = {
    "qualification.transaction_type": {
        "fr": "Souhaitez-vous louer, acheter ou vendre ?",
        "en": "Do you want to rent, buy or sell?",
        "pcm": "You want rent, buy or sell?",
    },
    "qualification.property_type": {
        "fr": "Quel type de bien recherchez-vous ?",
        "en": "What type of property are you looking for?",
        "pcm": "Wetin kind property you dey find?",
    },
    "qualification.city": {
        "fr": "Dans quelle ville ?",
        "en": "In which city?",
        "pcm": "Which city?",
    },
    "qualification.district": {
        "fr": "Dans quel quartier ?",
        "en": "In which district?",
        "pcm": "Which area?",
    },
    "qualification.budget": {
        "fr": "Quel est votre budget en francs CFA ?",
        "en": "What is your budget in CFA francs?",
        "pcm": "Your budget na how much for CFA?",
    },
    "qualification.bedrooms": {
        "fr": "Combien de chambres souhaitez-vous ?",
        "en": "How many bedrooms do you need?",
        "pcm": "How many bedrooms you want?",
    },
    "qualification.bathrooms": {
        "fr": "Combien de salles de bain ?",
        "en": "How many bathrooms?",
        "pcm": "How many bathroom?",
    },
    "qualification.kitchens": {
        "fr": "Combien de cuisines souhaitez-vous ?",
        "en": "How many kitchens do you need?",
        "pcm": "How many kitchen you want?",
    },
    "qualification.furnished": {
        "fr": "Souhaitez-vous un logement meublé ?",
        "en": "Do you want a furnished property?",
        "pcm": "You want property wey don get furniture?",
    },
    "qualification.move_in_date": {
        "fr": "À quelle date souhaitez-vous emménager ?",
        "en": "When would you like to move in?",
        "pcm": "Which date you want move enter?",
    },
    "qualification.other_requirements": {
        "fr": "Avez-vous d'autres critères ou exigences particulières ?",
        "en": "Do you have any other requirements?",
        "pcm": "You get any oda tings wey you want?",
    },
    "qualification.intended_use": {
        "fr": "Quel est l'usage prévu du terrain ?",
        "en": "What is the intended use of the land?",
        "pcm": "Wetin you go use di land do?",
    },
    "qualification.surface": {
        "fr": "Quelle surface souhaitez-vous en mètres carrés ?",
        "en": "What surface area do you need in square metres?",
        "pcm": "How many square metre you want?",
    },
    "qualification.title_status": {
        "fr": "Quel est le statut du titre foncier ?",
        "en": "What is the title deed status?",
        "pcm": "Wetin be di land paper status?",
    },
    "qualification.accessibility": {
        "fr": "Le terrain est-il accessible par la route ?",
        "en": "Is the land accessible by road?",
        "pcm": "Di land get road access?",
    },
    "qualification.utilities": {
        "fr": "Quels raccordements sont disponibles sur le terrain ?",
        "en": "What utilities are available on the land?",
        "pcm": "Wetin utilities dey for di land?",
    },
    "qualification.financing_mode": {
        "fr": "Quel mode de financement prévoyez-vous ?",
        "en": "What financing method do you plan to use?",
        "pcm": "How you go pay for am?",
    },
    "qualification.title_requirements": {
        "fr": "Avez-vous des exigences particulières concernant le titre foncier ?",
        "en": "Do you have any title deed requirements?",
        "pcm": "You get any special tings for di land paper?",
    },
    "qualification.actor_role": {
        "fr": "Êtes-vous le propriétaire ou un mandataire ?",
        "en": "Are you the owner or a representative?",
        "pcm": "You be di owner or you represent somebody?",
    },
    "qualification.ownership_status": {
        "fr": "Quel est votre statut de propriété ?",
        "en": "What is your ownership status?",
        "pcm": "Wetin be your ownership status?",
    },
    "qualification.documents_available": {
        "fr": "Quels documents avez-vous disponibles ?",
        "en": "What documents do you have available?",
        "pcm": "Wetin documents you get?",
    },
    "qualification.asking_price": {
        "fr": "Quel est votre prix de vente ?",
        "en": "What is your asking price?",
        "pcm": "How much you want sell am?",
    },
    "qualification.occupancy_status": {
        "fr": "Le bien est-il actuellement occupé ?",
        "en": "Is the property currently occupied?",
        "pcm": "Di property dey occupied now?",
    },
    "qualification.inspection_availability": {
        "fr": "Quand peut-on visiter le bien ?",
        "en": "When can the property be inspected?",
        "pcm": "When we fit come see di property?",
    },
    "qualification.monthly_rent": {
        "fr": "Quel est le loyer mensuel souhaité ?",
        "en": "What is the desired monthly rent?",
        "pcm": "How much you want for rent every month?",
    },
    "qualification.charges": {
        "fr": "Quel est le montant des charges ?",
        "en": "What is the amount of the charges?",
        "pcm": "How much be di charges?",
    },
    "qualification.availability_date": {
        "fr": "À quelle date le bien sera-t-il disponible ?",
        "en": "When will the property be available?",
        "pcm": "Which date di property go ready?",
    },
    "qualification.location": {
        "fr": "Où se situe le bien ?",
        "en": "Where is the property located?",
        "pcm": "Where di property dey?",
    },
    "qualification.price": {
        "fr": "Quel est le prix ?",
        "en": "What is the price?",
        "pcm": "How much?",
    },
    "qualification.description": {
        "fr": "Pouvez-vous décrire le bien ?",
        "en": "Can you describe the property?",
        "pcm": "You fit describe di property?",
    },
    "qualification.documents": {
        "fr": "Quels documents pouvez-vous fournir ?",
        "en": "What documents can you provide?",
        "pcm": "Wetin documents you fit give?",
    },
    "qualification.media": {
        "fr": "Avez-vous des photos ou vidéos du bien ?",
        "en": "Do you have photos or videos of the property?",
        "pcm": "You get photos or video of di property?",
    },
    "qualification.availability": {
        "fr": "Quand le bien est-il disponible ?",
        "en": "When is the property available?",
        "pcm": "When di property dey available?",
    },
    "qualification.consent": {
        "fr": "Acceptez-vous de publier cette annonce ?",
        "en": "Do you consent to publish this listing?",
        "pcm": "You agree make we post am?",
    },
    "qualification.property_reference": {
        "fr": "Quelle est la référence du bien ?",
        "en": "What is the property reference?",
        "pcm": "Wetin be di property reference?",
    },
    "qualification.preferred_date": {
        "fr": "Quelle date préférez-vous pour la visite ?",
        "en": "What date do you prefer for the visit?",
        "pcm": "Which date you want for di visit?",
    },
    "qualification.preferred_time_window": {
        "fr": "À quelle heure préférez-vous ?",
        "en": "What time do you prefer?",
        "pcm": "Which time you want?",
    },
    "qualification.contact_channel": {
        "fr": "Comment souhaitez-vous être contacté ?",
        "en": "How do you want to be contacted?",
        "pcm": "How you want make we contact you?",
    },
    "qualification.attendee_count": {
        "fr": "Combien de personnes participeront à la visite ?",
        "en": "How many people will attend the visit?",
        "pcm": "How many people go come for di visit?",
    },
    "qualification.confirmation": {
        "fr": "Confirmez-vous cette visite ?",
        "en": "Do you confirm this visit?",
        "pcm": "You confirm di visit?",
    },
    "qualification.document_type": {
        "fr": "De quel type de document s'agit-il ?",
        "en": "What type of document is it?",
        "pcm": "Wetin kind document be dis?",
    },
    "qualification.document_owner": {
        "fr": "À qui appartient ce document ?",
        "en": "Who owns this document?",
        "pcm": "Who get dis document?",
    },
    "qualification.requested_action": {
        "fr": "Que souhaitez-vous faire avec ce document ?",
        "en": "What do you want to do with this document?",
        "pcm": "Wetin you want do with dis document?",
    },
    "qualification.document_availability": {
        "fr": "Le document est-il disponible immédiatement ?",
        "en": "Is the document available immediately?",
        "pcm": "Di document dey available right now?",
    },
    "qualification.service_type": {
        "fr": "Quel type de service recherchez-vous ?",
        "en": "What type of service are you looking for?",
        "pcm": "Wetin kind service you dey find?",
    },
    "qualification.project_location": {
        "fr": "Où se situe le projet ?",
        "en": "Where is the project located?",
        "pcm": "Where di project dey?",
    },
    "qualification.project_stage": {
        "fr": "À quel stade en est le projet ?",
        "en": "What stage is the project at?",
        "pcm": "Which stage di project dey?",
    },
    "qualification.scope": {
        "fr": "Quelle est l'étendue des travaux ?",
        "en": "What is the scope of work?",
        "pcm": "How far di work go reach?",
    },
    "qualification.budget_range": {
        "fr": "Quelle est votre fourchette de budget ?",
        "en": "What is your budget range?",
        "pcm": "Your budget range na how much?",
    },
    "qualification.timeline": {
        "fr": "Quel est le calendrier prévu ?",
        "en": "What is the expected timeline?",
        "pcm": "When you want make di work finish?",
    },
    "qualification.preferred_contact": {
        "fr": "Comment préférez-vous être contacté ?",
        "en": "How do you prefer to be contacted?",
        "pcm": "How you like make we call you?",
    },
    # Clarification prompts
    "qualification.clarify.transaction_type": {
        "fr": "Souhaitez-vous louer un bien, en acheter un ou vendre une propriété ?",
        "en": "Do you want to rent a property, buy one, or sell a property?",
        "pcm": "You want rent property, buy property, or sell property?",
    },
    "qualification.clarify.property_type": {
        "fr": "Quel type de bien cherchez-vous ? Par exemple : appartement, studio, maison, terrain.",
        "en": "What type of property are you looking for? For example: apartment, studio, house, land.",
        "pcm": "Wetin kind property you dey find? Like apartment, studio, house, land.",
    },
    "qualification.clarify.city": {
        "fr": "Dans quelle ville ou localité se situe votre recherche ?",
        "en": "In which city or town is your search?",
        "pcm": "Which city or town you dey find?",
    },
    "qualification.clarify.district": {
        "fr": "Dans quel quartier précisément ?",
        "en": "In which specific neighbourhood?",
        "pcm": "Which exact area?",
    },
    "qualification.clarify.budget": {
        "fr": "Quel budget maximum avez-vous en tête ? Par exemple : 100 000 FCFA.",
        "en": "What is your maximum budget? For example: 100,000 CFA francs.",
        "pcm": "Your maximum budget na how much? For example: 100,000 CFA.",
    },
    "qualification.clarify.bedrooms": {
        "fr": "Combien de chambres à coucher avez-vous besoin ?",
        "en": "How many bedrooms do you require?",
        "pcm": "How many bedrooms you need?",
    },
    "qualification.clarify.bathrooms": {
        "fr": "Combien de salles de bain sont nécessaires ?",
        "en": "How many bathrooms are needed?",
        "pcm": "How many bathroom you need?",
    },
    "qualification.clarify.kitchens": {
        "fr": "Combien de cuisines avez-vous besoin ?",
        "en": "How many kitchens do you need?",
        "pcm": "How many kitchen you need?",
    },
    "qualification.clarify.furnished": {
        "fr": "Voulez-vous un bien meublé ou non meublé ?",
        "en": "Do you want a furnished or unfurnished property?",
        "pcm": "You want property wey get furniture or no get?",
    },
    "qualification.clarify.move_in_date": {
        "fr": "À partir de quand souhaitez-vous emménager ?",
        "en": "From when do you want to move in?",
        "pcm": "From which date you want move enter?",
    },
    "qualification.clarify.intended_use": {
        "fr": "Quel usage comptez-vous faire de ce terrain ?",
        "en": "What do you plan to use this land for?",
        "pcm": "Wetin you plan to use di land do?",
    },
    "qualification.clarify.surface": {
        "fr": "Quelle surface recherchez-vous en mètres carrés ?",
        "en": "What surface area in square metres are you looking for?",
        "pcm": "How many square metre you dey find?",
    },
    "qualification.clarify.title_status": {
        "fr": "Quel est le statut du titre de propriété ?",
        "en": "What is the status of the property title?",
        "pcm": "Wetin be di property title status?",
    },
    "qualification.clarify.accessibility": {
        "fr": "Le terrain est-il desservi par une route ?",
        "en": "Is the land served by a road?",
        "pcm": "Di land get road wey dey serve am?",
    },
    "qualification.clarify.utilities": {
        "fr": "Quels sont les raccordements disponibles (eau, électricité, internet) ?",
        "en": "What connections are available (water, electricity, internet)?",
        "pcm": "Wetin connections dey (water, light, internet)?",
    },
    "qualification.clarify.financing_mode": {
        "fr": "Comment comptez-vous financer cet achat ?",
        "en": "How do you plan to finance this purchase?",
        "pcm": "How you go pay for dis purchase?",
    },
    "qualification.clarify.title_requirements": {
        "fr": "Avez-vous des exigences particulières sur le titre ?",
        "en": "Do you have specific requirements on the title?",
        "pcm": "You get special requirements for di title?",
    },
    "qualification.clarify.actor_role": {
        "fr": "Êtes-vous le propriétaire direct ou un intermédiaire ?",
        "en": "Are you the direct owner or an intermediary?",
        "pcm": "You be di owner direct or you na middle person?",
    },
    "qualification.clarify.ownership_status": {
        "fr": "Quel est votre lien avec ce bien ?",
        "en": "What is your relationship to this property?",
        "pcm": "Wetin be your relationship with dis property?",
    },
    "qualification.clarify.documents_available": {
        "fr": "De quels documents disposez-vous pour ce bien ?",
        "en": "What documents do you have for this property?",
        "pcm": "Wetin documents you get for dis property?",
    },
    "qualification.clarify.asking_price": {
        "fr": "À quel prix souhaitez-vous vendre ?",
        "en": "At what price do you want to sell?",
        "pcm": "How much you want sell am?",
    },
    "qualification.clarify.occupancy_status": {
        "fr": "Le bien est-il libre ou occupé actuellement ?",
        "en": "Is the property vacant or currently occupied?",
        "pcm": "Di property dey empty or get person wey dey stay?",
    },
    "qualification.clarify.monthly_rent": {
        "fr": "Quel loyer mensuel envisagez-vous ?",
        "en": "What monthly rent do you have in mind?",
        "pcm": "How much rent every month you dey tink?",
    },
    "qualification.clarify.charges": {
        "fr": "Quel est le montant des charges locatives ?",
        "en": "What is the amount of the rental charges?",
        "pcm": "How much be di rental charges?",
    },
    "qualification.clarify.availability_date": {
        "fr": "À partir de quelle date le bien est-il disponible ?",
        "en": "From what date is the property available?",
        "pcm": "From which date di property dey available?",
    },
    "qualification.clarify.location": {
        "fr": "Où se trouve exactement le bien ?",
        "en": "Where exactly is the property located?",
        "pcm": "Where di property dey exactly?",
    },
    "qualification.clarify.price": {
        "fr": "Quel est le montant exact ?",
        "en": "What is the exact amount?",
        "pcm": "How much be di exact amount?",
    },
    "qualification.clarify.description": {
        "fr": "Pouvez-vous décrire le bien en quelques mots ?",
        "en": "Can you describe the property in a few words?",
        "pcm": "You fit describe di property small?",
    },
    "qualification.clarify.documents": {
        "fr": "Quels documents pouvez-vous joindre ?",
        "en": "What documents can you attach?",
        "pcm": "Wetin documents you fit attach?",
    },
    "qualification.clarify.media": {
        "fr": "Avez-vous des éléments visuels à partager ?",
        "en": "Do you have visual materials to share?",
        "pcm": "You get visual materials wey you fit share?",
    },
    "qualification.clarify.availability": {
        "fr": "Quand le bien peut-il être visité ?",
        "en": "When can the property be viewed?",
        "pcm": "When we fit come see di property?",
    },
    "qualification.clarify.consent": {
        "fr": "Confirmez-vous votre accord pour cette action ?",
        "en": "Do you confirm your consent for this action?",
        "pcm": "You agree for dis action?",
    },
    "qualification.clarify.property_reference": {
        "fr": "Quelle est la référence ou l'adresse du bien ?",
        "en": "What is the property reference or address?",
        "pcm": "Wetin be di property reference or address?",
    },
    "qualification.clarify.preferred_date": {
        "fr": "Quelle date vous conviendrait pour la visite ?",
        "en": "What date would work for the visit?",
        "pcm": "Which date go work for di visit?",
    },
    "qualification.clarify.preferred_time_window": {
        "fr": "Quelle tranche horaire préférez-vous ?",
        "en": "What time window do you prefer?",
        "pcm": "Which time you prefer?",
    },
    "qualification.clarify.contact_channel": {
        "fr": "Par quel moyen souhaitez-vous être contacté ?",
        "en": "How would you like to be contacted?",
        "pcm": "How you want make we contact you?",
    },
    "qualification.clarify.attendee_count": {
        "fr": "Combien de personnes seront présentes ?",
        "en": "How many people will be present?",
        "pcm": "How many people go dey?",
    },
    "qualification.clarify.confirmation": {
        "fr": "Pouvez-vous confirmer votre intention ?",
        "en": "Can you confirm your intention?",
        "pcm": "You fit confirm wetin you want?",
    },
    "qualification.clarify.document_type": {
        "fr": "De quel document s'agit-il ?",
        "en": "What document is this?",
        "pcm": "Wetin document be dis?",
    },
    "qualification.clarify.document_owner": {
        "fr": "À qui appartient ce document ?",
        "en": "Who does this document belong to?",
        "pcm": "Who get dis document?",
    },
    "qualification.clarify.requested_action": {
        "fr": "Que voulez-vous faire avec ce document ?",
        "en": "What do you want to do with this document?",
        "pcm": "Wetin you want do with dis document?",
    },
    "qualification.clarify.document_availability": {
        "fr": "Le document est-il disponible dès maintenant ?",
        "en": "Is the document available right now?",
        "pcm": "Di document dey available right now?",
    },
    "qualification.clarify.service_type": {
        "fr": "Quel service recherchez-vous exactement ?",
        "en": "What service are you looking for exactly?",
        "pcm": "Wetin kind service you dey find exactly?",
    },
    "qualification.clarify.project_location": {
        "fr": "Où se déroulera le projet ?",
        "en": "Where will the project take place?",
        "pcm": "Where di project go take place?",
    },
    "qualification.clarify.project_stage": {
        "fr": "À quelle étape du projet êtes-vous ?",
        "en": "What stage of the project are you at?",
        "pcm": "Which stage of di project you dey?",
    },
    "qualification.clarify.scope": {
        "fr": "Quelle est l'ampleur des travaux à réaliser ?",
        "en": "What is the scope of the work to be done?",
        "pcm": "How big be di work wey you want do?",
    },
    "qualification.clarify.budget_range": {
        "fr": "Quelle fourchette de budget envisagez-vous ?",
        "en": "What budget range do you have in mind?",
        "pcm": "How much budget you dey tink?",
    },
    "qualification.clarify.timeline": {
        "fr": "Quel est le calendrier souhaité pour ce projet ?",
        "en": "What is the desired timeline for this project?",
        "pcm": "When you want make di project finish?",
    },
    "qualification.clarify.preferred_contact": {
        "fr": "Comment souhaitez-vous que l'on vous contacte ?",
        "en": "How would you like us to contact you?",
        "pcm": "How you want make we call you?",
    },
}


def get_question(key: str, language: str = "fr") -> str:
    entry = QUESTION_CATALOG.get(key)
    if entry is None:
        return ""
    return entry.get(language, entry.get("fr", ""))


def get_clarification(key: str, language: str = "fr") -> str:
    clarification_key = key.replace("qualification.", "qualification.clarify.")
    if clarification_key == key:
        clarification_key = f"qualification.clarify.{key.split('.')[-1]}"
    entry = QUESTION_CATALOG.get(clarification_key)
    if entry is None:
        return get_question(key, language)
    return entry.get(language, entry.get("fr", ""))


def has_language(key: str, language: str) -> bool:
    entry = QUESTION_CATALOG.get(key)
    if entry is None:
        return False
    return language in entry
