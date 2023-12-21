import { LabIcon } from '@jupyterlab/ui-components';

import smceServicesSVG from '../../style/SMCE_Services_Logo.svg';
import voiceAtlasIconSVG from '../../style/voiceatlas_logo.svg';
import voiceAtlasWordmarkIconSVG from '../../style/VoiceAtlas_Wordmark.svg'

export const voiceAtlasIcon = new LabIcon({ name: 'logo', svgstr: voiceAtlasIconSVG });
export const voiceAtlasWordmarkIcon = new LabIcon({ name: 'wordmark', svgstr: voiceAtlasWordmarkIconSVG });
export const smceServicesIcon = new LabIcon({ name: 'smce:logo', svgstr: smceServicesSVG });
