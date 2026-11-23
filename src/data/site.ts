// All company facts live here, so they are edited in one place.

export const company = {
  name: 'Pro-Revisjon AS',
  shortName: 'Pro-Revisjon',
  url: 'https://pro-revisjon.no',
  street: 'Kongsgård Alle 61',
  postalCode: '4632',
  city: 'Kristiansand',
  phone: { display: '38 14 44 44', href: 'tel:+4738144444', schema: '+47 38 14 44 44' },
  fax: '38 14 44 50',
  email: 'firmapost@pro-revisjon.no',
  mapUrl:
    'https://www.google.com/maps/search/?api=1&query=Kongsg%C3%A5rd+All%C3%A9+61%2C+4632+Kristiansand',
};

export type Person = {
  name: string;
  /** File name (without extension) in src/assets/images/ansatte/. Shows initials until the file exists. */
  photo: string;
  title: string;
  mobile: { display: string; href: string };
  email: string;
};

export const people: Person[] = [
  {
    name: 'Øystein Enger',
    photo: 'oystein',
    title: 'Statsautorisert revisor / autorisert regnskapsfører',
    mobile: { display: '90 66 64 01', href: 'tel:+4790666401' },
    email: 'oenger@pro-revisjon.no',
  },
  {
    name: 'Bernt Atle Enger',
    photo: 'bernt',
    title: 'Statsautorisert revisor / autorisert regnskapsfører',
    mobile: { display: '90 66 64 05', href: 'tel:+4790666405' },
    email: 'baenger@pro-revisjon.no',
  },
  {
    name: 'Morten Endre Lohne',
    photo: 'morten',
    title: 'Revisormedarbeider',
    mobile: { display: '95 72 32 32', href: 'tel:+4795723232' },
    email: 'melohne@pro-revisjon.no',
  },
];

export type Service = {
  slug: string;
  title: string;
  /** One short line, used only in the homepage list. */
  tagline: string;
  /** One sentence, used only on the services overview and as the service page lead. */
  lead: string;
  /** Photo slot name in src/assets/images/photos/ */
  photo: string;
  photoAlt: string;
  photoFocus: 'center' | 'left' | 'right' | 'top' | 'bottom' | 'bottom-left' | 'bottom-right' | 'top-right';
};

export const services: Service[] = [
  {
    slug: 'revisjon',
    title: 'Revisjon',
    tagline: 'Lovpålagt revisjon og attestasjon',
    lead: 'Lovbestemt revisjon er vår hovedvirksomhet – utført av statsautoriserte revisorer.',
    photo: 'arbeidsplass-1',
    photoAlt: 'Kalkulator, notatbok og bærbar PC på et skrivebord i eik',
    photoFocus: 'bottom-left',
  },
  {
    slug: 'regnskap-og-skatt',
    title: 'Regnskap og skatt',
    tagline: 'Årsregnskap, skattemelding og avgift',
    lead: 'Vi utarbeider årsregnskap og skattemelding, og hjelper med skatte- og avgiftsspørsmål.',
    photo: 'arbeidsplass-2',
    photoAlt: 'Bærbar PC med regnskapstall, kalkulator og notatbok',
    photoFocus: 'right',
  },
  {
    slug: 'radgivning',
    title: 'Rådgivning',
    tagline: 'Selskapsform, generasjonsskifte og verdivurdering',
    lead: 'Rådgivning for selskaper, institusjoner og privatpersoner – ofte i samarbeid med advokater og meglere.',
    photo: 'gjennomgang',
    photoAlt: 'To personer går gjennom tall og dokumenter ved et bord',
    photoFocus: 'center',
  },
];

export const usefulLinks = [
  {
    group: 'Offentlige etater og registre',
    links: [
      { name: 'Skatteetaten', url: 'https://www.skatteetaten.no/', note: 'Skatt, avgift og skattemelding' },
      { name: 'Altinn', url: 'https://www.altinn.no/', note: 'Innrapportering til det offentlige' },
      { name: 'Brønnøysundregistrene', url: 'https://www.brreg.no/', note: 'Foretaksregister og offentlige registre' },
      { name: 'Regjeringen.no', url: 'https://www.regjeringen.no/', note: 'Departementene (tidligere ODIN)' },
      { name: 'Statistisk sentralbyrå', url: 'https://www.ssb.no/', note: 'Offisiell statistikk' },
    ],
  },
  {
    group: 'Fag og regelverk',
    links: [
      { name: 'Lovdata', url: 'https://lovdata.no/', note: 'Lover og forskrifter' },
      { name: 'Revisorforeningen', url: 'https://www.revisorforeningen.no/', note: 'Den Norske Revisorforening' },
      { name: 'Aktuelle satser', url: 'https://www.aktuellesatser.no/pro-revisjon', note: 'Oppdaterte satser og grenser' },
    ],
  },
];

/** Main navigation. `match` marks the item as active for every page under that path. */
export const nav = [
  { href: '/tjenester/', label: 'Tjenester' },
  { href: '/om-oss/', label: 'Om oss' },
  { href: '/ansatte/', label: 'Ansatte' },
  { href: '/kontakt/', label: 'Kontakt' },
];

export function firstName(name: string) {
  return name.split(' ')[0];
}

export function initials(name: string) {
  const parts = name.split(' ');
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}
