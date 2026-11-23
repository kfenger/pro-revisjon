# Endringslogg

Alle vesentlige endringer i nettsiden føres her. Versjonene følger [semantisk versjonering](https://semver.org/lang/no/):
MAJOR for store omlegginger, MINOR for nye funksjoner eller synlige forbedringer, PATCH for rettelser.

## [1.1.0] – 2026-11-23

### Endret
- Footeren er mindre og roligere: «Skal vi ta en prat?», telefonnummer og luft er nedskalert.

### Lagt til
- Mobilmenyen lukkes når man trykker utenfor menyen (uten JavaScript), med en svak nedtoning av siden bak.
- Testpakken ligger nå i `tests/`.

### Rettet
- Tjenester-siden: listen sto helt inntil venstre kant på mobil. Den følger nå samme marg som resten av siden.

## [1.0.0] – 2026-11-23

### Lagt til
- Første versjon av den nye nettsiden: flersidestruktur (forside, tjenester med tre undersider, om oss, ansatte,
  kontakt, nyttige lenker, personvern), ekte logo og fotografier, rolig skandinavisk designsystem.
- Statisk Astro-side uten JavaScript, streng sikkerhetsprofil (CSP m.m.) og generert `.htaccess`, `_headers`, `_redirects`.
- GitHub Pages-workflow for testversjon (noindex og egen `robots.txt`).

[1.1.0]: https://github.com/kfenger/pro-revisjon/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/kfenger/pro-revisjon/releases/tag/v1.0.0
