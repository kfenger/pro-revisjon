# Endringslogg

Alle vesentlige endringer i nettsiden føres her. Versjonene følger [semantisk versjonering](https://semver.org/lang/no/):
MAJOR for store omlegginger, MINOR for nye funksjoner eller synlige forbedringer, PATCH for rettelser.

## [1.3.0] – 2026-11-23

### Endret
- Forsiden: på PC er det nå bare én «Ta kontakt»-knapp i toppen. På mobil er «eller ring» erstattet med en egen «Ring 38 14 44 44»-knapp.
- Forsiden: tjenestedelen har fått en ordentlig overskrift og lenken «Alle tjenester» i stedet for en ensom etikett.
- Tjenester-siden: på PC vises de tre tjenestene i tre kolonner med bilde, tittel og kort beskrivelse.
- Tjenestesidene: innholdet står i to kolonner ved siden av hverandre, med «Andre tjenester» tettere inntil. Toppbildet er lavere.
- Om oss: roligere tekststørrelse, synlig overskrift over «Slik arbeider vi» og en slankere avslutning.
- Kontakt: bildet er større og står på linje med kontaktinformasjonen.
- Generelt strammere luft mellom seksjonene på PC.

## [1.2.0] – 2026-11-23

### Endret (kun PC – mobil og nettbrett er uendret)
- Innholdet bruker nå hele skjermbredden med marg på sidene, i stedet for en fast stripe på 1200 px.
- Hele grensesnittet skalerer med skjermen: litt større tekst og avstander fra 1440 px og 1920 px.
- Menylinjen strekker seg over hele bredden, og telefonnummeret er fjernet fra den.
- Forsiden: slideshowet ligger innenfor sidemargen med luft rundt, i stedet for å gå ut til kanten.
- «Kort vei til revisoren»: bildet følger samme marg som resten av siden.
- Tjenestesidene: «Andre tjenester» vises som en sidekolonne i stedet for under innholdet.
- Footeren er midtstilt, med kontaktfeltene «Ring oss», «Send e-post» og «Besøk oss» side om side.

### Fjernet
- Pauseknappen på slideshowet (gjelder også mobil). Med «redusert bevegelse» vises fortsatt bare ett stillbilde.

## [1.1.0] – 2026-11-23

### Endret
- Footeren er mindre og roligere: «Skal vi ta en prat?», telefonnummer og luft er nedskalert.

### Lagt til
- Mobilmenyen lukkes når man trykker utenfor menyen (uten JavaScript), med en svak nedtoning av siden bak.
- Testpakken ligger nå i `tests/`.
- Automatisk versjonering: hver versjon i `package.json` får en git-tagg og en GitHub Release med teksten herfra.

### Rettet
- Tjenester-siden: listen sto helt inntil venstre kant på mobil. Den følger nå samme marg som resten av siden.

## [1.0.0] – 2026-11-23

### Lagt til
- Første versjon av den nye nettsiden: flersidestruktur (forside, tjenester med tre undersider, om oss, ansatte,
  kontakt, nyttige lenker, personvern), ekte logo og fotografier, rolig skandinavisk designsystem.
- Statisk Astro-side uten JavaScript, streng sikkerhetsprofil (CSP m.m.) og generert `.htaccess`, `_headers`, `_redirects`.
- GitHub Pages-workflow for testversjon (noindex og egen `robots.txt`).

[1.3.0]: https://github.com/kfenger/pro-revisjon/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/kfenger/pro-revisjon/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/kfenger/pro-revisjon/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/kfenger/pro-revisjon/releases/tag/v1.0.0
