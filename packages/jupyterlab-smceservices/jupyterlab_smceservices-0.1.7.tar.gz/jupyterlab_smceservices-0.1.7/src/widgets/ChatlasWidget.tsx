import { Widget } from '@lumino/widgets';

export class ChatlasWidget extends Widget {
    constructor(atlasId: string) {
        const script = document.createElement('script')
        script.setAttribute("src", "https://bot.voiceatlas.mysmce.com/v1/chatlas.js")
        script.setAttribute("async", "")
        document.body.appendChild(script)

        const chatlas = document.createElement('app-chatlas')
        chatlas.setAttribute("atlas-id", atlasId)
        chatlas.setAttribute("full-screen", "true")
        chatlas.setAttribute("widget-background-color", "#3f51b5ff")
        chatlas.setAttribute("widget-text-color", "#ffffffff")
        chatlas.setAttribute("widget-title", "Chatlas")
        super({ node: chatlas })
    }
}