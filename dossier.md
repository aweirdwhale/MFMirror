![banner](https://raw.githubusercontent.com/aweirdwhale/MFMirror/dev/Explainations/assets/readmebanner.png)

# **MFMirror**

_**Par Les Biquettes**_
_"Les Biquettes" est le nom donné au groupe de Baptiste et Olivier dans leur aventure Numérique._

## Table des matières

* **[Synopsis](#Synopsis)**
* **[Les 5 w](#Les-5-w)**
* **[Le chemin parcouru](#docs)**
* **[Le reste à faire](#todo)**
* **[Conclusion](#conclu)**

---

### Synopsis

Vous n'avez pas d'amis ? Mieux qu'un curly : MFMirror !
 
Hermione est une intelligence artificielle, créée par les Biquettes. Elle alimente le meilleur miroir du monde : MFMirror. Si je devais résumer MFMirror avec vous aujourd'hui, je commencerais par dire que c'est une rencontre entre deux esprits brillants. Et c'est assez curieux de penser que cette rencontre fortuite a forgé un des meilleurs miroirs, car lorsque vous avez ce goût pour les choses bien faites, le beau geste, eh bien je dirais que vous ne trouverez pas d'intérêt à espionner vos clients comme le font nos concurrents Amazon, Google ou même Apple.

Ainsi, comme vous l'aurez compris, Les Biquettes présentent aujourd'hui un projet né d'une rencontre entre les esprits les plus éminents de la science-fiction et ceux des Frères Grimm.

En apparence simple mais fascinant, le miroir est, en fait, un instrument merveilleux qui a captivé l'imagination des gens pendant des siècles, possédant une aura mystique à la fois pratique et magique, le rendant unique parmi les objets de tous les jours. Allié à l'intelligence artificielle, dont nous parlons trop ces derniers temps.

MFMirror est un prototype de miroir basé sur J.A.R.V.I.S, l'IA du célèbre personnage fictif Tony Stark, alias Iron Man, ou de Gideon, l'IA de Barry Allen, alias Flash.

Une synthèse vocale vous permettra d'entrer en communication, et la reconnaissance faciale donnera à l'utilisateur un sentiment de proximité.

Sans clavier, ni souris, ni autres périphériques, le miroir pourra être contrôlé par la voix ou les gestes de la main. Il affichera ce que vous lui demanderez, grâce à un écran caché derrière un miroir sans tain. Il est alimenté par batterie et en veille, il affichera l'heure, la météo et pourra gérer votre musique depuis Internet ou stockée localement.
Enfin, en utilisant un logiciel propriétaire, il pourra gérer votre emploi du temps, un minuteur et bien plus encore sans utiliser de services tiers. La caméra ne sera pas du tout connectée à Internet, pour éviter les logiciels espions.

Les Biquettes font un point d'honneur à protéger vos informations personnelles (vraiment !), et 95 % des informations nécessaires au bon fonctionnement de l'appareil seront stockées localement, à l'abri des publicitaires malveillants et des pirates.

---

### Les 5 w :

1. **Pour qui ?**
   * Pour tous, n'importe qui ! MFMirror est destiné à n'importe qui voudrait l'essayer. Et sans avoir de miroir il est toujours possible d'utiliser Hermione sur un ordinateur normal !
2. **Pourquoi ?**
   * La première réponse qui nous vient à l'esprit est "Pourquoi pas ?", en effet toute personne sensée trouverait cette invention inutile et dépourvue de sens, mais de notre point de vue, c'est une merveille de code et de construction. En dépit de son inutilité, Hermione nous à permis d'en apprendre plus sur la reconnaissance faciale, gestuelle et vocale, sur la programmation orientée objet et sur la construction d'objets physiques.
   * _Fait rigolo : Hermione et MFMirror en cumulé font plus de 200 000 lignes de code !_
3. **Quand ?**
   * Hermione v-alpha est terminée ! La release est disponible [ici](https://github.com/aweirdwhale/MFMirror) !
   * Le projet complet MFM est, lui, prevu vers la fin Mars 2024.
4. **Où ?**
   * Le projet est accessible à l'utilisation et à la contribution n'importe où dans le monde !
   * Si vous avez envie de participer, tout est [ici](https://github.com/aweirdwhale/MFMirror) !

---

### Le chemin parcouru :

La première étape a été la conceptualisation de l'idée.

Notre parcours dans ce projet a été une véritable aventure, pleine d'étapes cruciales et de défis stimulants. Tout a commencé avec la phase de _proof of concept_, où nous avons mis en œuvre nos premières idées pour voir si elles tenaient la route. Cette étape nous a permis de confirmer que notre projet était faisable.


Ensuite, nous nous sommes plongés dans le processus de conception en utilisant Figma, un outil puissant qui nous a aidé à concrétiser nos idées sous forme de maquettes interactives. Cela nous a permis de mieux visualiser et affiner notre vision du produit final.
![Capture d'écran de Figma](https://github.com/aweirdwhale/MFMirror/raw/mfm/Explainations/assets/CaptureFigma.PNG?raw=true)

L'intégration de la reconnaissance vocale avec le module _voice_recognition_ et la création d'un système de réveil avec _porcupine_ ont été des étapes importantes dans notre progression. Ces fonctionnalités ont rendu notre projet plus convivial et intuitif pour les utilisateurs.

```python
import speech_recognition as sr
```

*Ici, on peut voir la classe qui gère la reconnaissance vocale.  En premier lieu elle écoute, puis elle convertit, puis elle reconnaît grâce à l'api de google.*![Capture d'écran du code](https://raw.githubusercontent.com/aweirdwhale/MFMirror/dev/Explainations/assets/code_stt.png)

Les premières commandes ont marqué le début de l'interaction réelle avec notre système. C'est là que nous avons pu tester et ajuster notre code pour garantir un fonctionnement sans accroc.
[Vidéo de démonstration (Youtube)](https://youtu.be/m2F-8MmrUC8)

L'interface utilisateur, développée avec tkinter, a été soigneusement conçue pour offrir une expérience optimale aux utilisateurs. Chaque détail a été pensé pour faciliter l'interaction et la navigation dans notre système.

_création d'une interface simple avec tkinter_
![Capture d'écran du code et de l'interface utilisateur](https://raw.githubusercontent.com/aweirdwhale/MFMirror/dev/Explainations/assets/screencodeui.png)
![Capture de l'UI](https://raw.githubusercontent.com/aweirdwhale/MFMirror/dev/Explainations/assets/screen%20ui.png)

Les finitions ont été une étape cruciale pour peaufiner notre projet. Nous avons apporté des ajustements esthétiques et fonctionnels, ajouté des éléments tels que des salutations et des sons pour rendre l'expérience utilisateur encore plus immersive et agréable.
[Vidéo de démonstration (Youtube)](https://youtu.be/SJMAKETeiYE)

En parallèle, nous avons également développé des fonctionnalités techniques telles que la mise à jour automatique et l'arrêt du système pour améliorer la performance et la fiabilité de notre produit.

*ici le systeme de mises à jour : on regarde si la version correspond à celle de l'api sinon on télécharge le zip via le lien, on dé-zip en écrasant les ancien fichiers et on suprime le zip pour gagner de la place*
![Capture d'écran du code](https://raw.githubusercontent.com/aweirdwhale/MFMirror/dev/Explainations/assets/update.png)

Enfin, nous avons abordé la partie matérielle de notre projet en réparant un écran de récupération, en réalisant un montage soigné et en intégrant un Raspberry Pi pour garantir le bon fonctionnement de notre système.
![Photos de l'écran](https://media.discordapp.net/attachments/1132396777056772146/1216845843353702543/IMG_20240311_010253245.jpg?ex=6601df00&is=65ef6a00&hm=4c4d31d230eaaa8ba01f3e15fd52f61a18155a8173480a753e9db48c924c05e7&=&format=webp&width=468&height=468)

Dans l'ensemble, ce projet a été une expérience enrichissante, remplie de défis et de réussites. Chaque étape nous a rapprochés de notre objectif final avec confiance et détermination.

---

### Le reste à faire :

Il ne reste plus qu'à finaliser le montage Hardware, nous attendons la pièce maîtresse : le miroir

---

### Conclusion :

En résumé, notre projet de miroir connecté combine l'esthétisme et la fonctionnalité pour créer une expérience unique. Il simplifie la routine quotidienne en offrant la reconnaissance faciale, des options musicales, un accès quasi-instantané à Wikipédia et des informations météorologiques.
Un miroir qui va au-delà de la simple réflexion pour devenir un véritable assistant personnel, fruit du travail collaboratif de notre équipe.

Baptiste et Olivier

![Alex](https://www.programme-tv.net/imgre/fit/http.3A.2F.2Fprd2-bone-image.2Es3-website-eu-west-1.2Eamazonaws.2Ecom.2Ftel.2F2019.2F07.2F01.2F82b6a3a2-341b-439c-a922-5127f7fbc38c.2Ejpeg/720x405/crop-from/top/quality/80/alexandre-le-bienheureux.jpg)

##### PS:

Le projet est sous une licence MIT, donc ouvert à tous dans l'édition, la commercialisation ou l'utilisation personnelle, nous demandons simplement une rétribution.

Les polices utilisées dans l'UI : [Pilowlava](https://www.freefaces.gallery/typefaces/pilowlava) & [Subjectivity](https://www.freefaces.gallery/typefaces/subjectivity)

Entièremet codé en python.
