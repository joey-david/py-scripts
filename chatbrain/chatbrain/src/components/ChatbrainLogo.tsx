// filepath: /home/joey/Projects/py-scripts/chatbrain/chatbrain/src/components/ChatbrainLogo.tsx
import React from 'react'
import chatbrainLogo from '@/assets/chatbrain_logo.png'

const ChatbrainLogo: React.FC = () => {
  return <img src={chatbrainLogo} alt="Chatbrain Logo" className="h-12 w-auto" />
}

export default ChatbrainLogo