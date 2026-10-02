class ErreurFormatJSON(Exception):
    """Exception levée quand un fichier JSON de données ne respecte pas le format attendu."""

    def __init__(self, message: str, fichier: str = None):
        """Initialise l'exception.

        Args:
            message: Détail de ce qui ne va pas.
            fichier: Chemin du fichier concerné (optionnel, pour contexte).
        """
        self.fichier = fichier
        if fichier:
            super().__init__(f"[{fichier}] {message}")
        else:
            super().__init__(message)