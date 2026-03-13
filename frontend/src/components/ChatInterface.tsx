'use client';

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, User, Bot, RefreshCw, ChevronRight, BookOpen, ChevronDown, ListChecks } from 'lucide-react';
import { cn } from '@/lib/utils';
import { processMessage, fetchScripts, fetchScriptDetails } from '@/services/api';

interface Message {
  role: 'user' | 'avatar';
  content: string;
  thought?: string;
  action?: string;
}

interface Script {
  id: string;
  title: string;
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState('');
  const [userName, setUserName] = useState('');
  const [scripts, setScripts] = useState<Script[]>([]);
  const [selectedScript, setSelectedScript] = useState<string | null>(null);
  const [expandedScriptId, setExpandedScriptId] = useState<string | null>(null);
  const [scriptDetails, setScriptDetails] = useState<Record<string, any>>({});
  const [step, setStep] = useState<'selection' | 'chat'>('selection');
  const [isSessionFinished, setIsSessionFinished] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Initialize session & fetch scripts
  useEffect(() => {
    const storedName = localStorage.getItem('ai_avatar_user_name');
    if (storedName) setUserName(storedName);

    let storedId = localStorage.getItem('ai_avatar_session_id');
    if (!storedId) {
      const namePrefix = storedName ? `${storedName.toLowerCase().replace(/\s+/g, '_')}_` : '';
      storedId = namePrefix + 'session_' + Math.random().toString(36).substring(7);
      localStorage.setItem('ai_avatar_session_id', storedId);
    }
    setSessionId(storedId);

    const loadScripts = async () => {
      try {
        const data = await fetchScripts();
        setScripts(data);
      } catch (error) {
        console.error("Failed to load scripts", error);
      }
    };
    loadScripts();
  }, []);

  // Scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || isLoading || isSessionFinished) return;

    const userMsg = input.trim();
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: userMsg }]);
    setIsLoading(true);

    try {
      const result = await processMessage({
        session_id: sessionId,
        user_input: userMsg,
        user_name: userName || undefined,
        script_name: selectedScript || undefined
      });

      if (result.is_completed) {
        setIsSessionFinished(true);
      }

      setMessages((prev) => [
        ...prev,
        {
          role: 'avatar',
          content: result?.brain_decision?.avatar_response || result?.message || "I've processed your message.",
          thought: result?.brain_decision?.thought_process,
          action: result?.brain_decision?.action,
        },
      ]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { role: 'avatar', content: "I'm sorry, I'm having trouble connecting right now. Please try again." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const startSession = (scriptTitle: string) => {
    if (!userName.trim()) {
      alert("Please enter your name first.");
      return;
    }
    
    // Ensure session ID includes name for better visibility in Firestore
    const namePrefix = userName.toLowerCase().replace(/\s+/g, '_');
    if (!sessionId.startsWith(namePrefix)) {
      const newId = `${namePrefix}_session_${Math.random().toString(36).substring(7)}`;
      setSessionId(newId);
      localStorage.setItem('ai_avatar_session_id', newId);
    }

    localStorage.setItem('ai_avatar_user_name', userName);
    setSelectedScript(scriptTitle);
    setStep('chat');
    setIsSessionFinished(false);
  };

  const resetSession = () => {
    const namePrefix = userName ? `${userName.toLowerCase().replace(/\s+/g, '_')}_` : '';
    const newId = namePrefix + 'session_' + Math.random().toString(36).substring(7);
    localStorage.setItem('ai_avatar_session_id', newId);
    setSessionId(newId);
    setMessages([]);
    setStep('selection');
    setSelectedScript(null);
    setExpandedScriptId(null);
    setIsSessionFinished(false);
  };

  const toggleScriptExpansion = async (scriptId: string) => {
    if (expandedScriptId === scriptId) {
      setExpandedScriptId(null);
      return;
    }

    setExpandedScriptId(scriptId);

    // Fetch details if not already cached
    if (!scriptDetails[scriptId]) {
      try {
        const data = await fetchScriptDetails(scriptId);
        setScriptDetails(prev => ({ ...prev, [scriptId]: data }));
      } catch (error) {
        console.error("Failed to fetch script details", error);
      }
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto bg-white shadow-2xl border-x overflow-hidden animate-in fade-in duration-700">
      {/* Header */}
      <header className="p-5 border-b flex justify-between items-center bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-500 text-white shadow-md z-10">
        <div className="flex items-center gap-3">
          <div className="bg-white/20 p-2 rounded-xl backdrop-blur-sm border border-white/30">
            <Bot size={24} className="text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight">AI Reflection</h1>
            <div className="flex items-center gap-1.5">
              <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
              <p className="text-[11px] font-medium text-white/80 uppercase tracking-wider">{step === 'chat' ? selectedScript : 'Ready to Start'}</p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {step === 'chat' && (
            <button 
              onClick={resetSession}
              className="p-2.5 hover:bg-white/10 rounded-xl transition-all active:scale-95 group text-white/90 hover:text-white"
              title="Reload Conversation"
            >
              <RefreshCw size={20} className="group-hover:rotate-180 transition-transform duration-500" />
            </button>
          )}
          <button 
            onClick={() => {
              if (confirm("Are you sure you want to end this reflection session?")) {
                resetSession();
              }
            }}
            className="px-4 py-2 bg-white/10 hover:bg-red-500/80 rounded-xl text-xs font-bold transition-all active:scale-95 border border-white/20"
          >
            End Session
          </button>
        </div>
      </header>

      {/* Main Content Areas */}
      <AnimatePresence mode="wait">
        {step === 'selection' ? (
          <motion.div
            key="selection"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            className="flex-1 overflow-y-auto p-8 space-y-8 bg-slate-50"
          >
            <div className="text-center space-y-4">
              <div className="bg-indigo-100 w-20 h-20 rounded-3xl flex items-center justify-center mx-auto shadow-inner text-indigo-600">
                <BookOpen size={40} />
              </div>
              <h2 className="text-2xl font-black text-slate-800">Select Your Path</h2>
              <p className="text-slate-500 text-sm">First, tell us your name, then choose a theme.</p>
            </div>

            <div className="max-w-md mx-auto w-full space-y-4">
              <div className="space-y-2">
                <label htmlFor="userName" className="text-xs font-bold uppercase tracking-widest text-slate-400 ml-1">Your Name</label>
                <input
                  id="userName"
                  type="text"
                  value={userName}
                  onChange={(e) => setUserName(e.target.value)}
                  placeholder="Enter your name..."
                  className="w-full px-6 py-4 bg-white border-2 border-slate-100 rounded-2xl text-sm font-medium focus:border-indigo-500 transition-all outline-none text-slate-800"
                />
              </div>
            </div>

            <div className="grid gap-4">
              {scripts.map((script) => (
                <div key={script.id} className="space-y-2">
                  <div className={cn(
                    "flex flex-col bg-white border-2 rounded-3xl transition-all overflow-hidden",
                    expandedScriptId === script.id ? "border-indigo-500 shadow-xl shadow-indigo-500/10" : "border-slate-100 hover:border-slate-300"
                  )}>
                    <div className="flex items-center justify-between p-5">
                      <button
                        onClick={() => startSession(script.title)}
                        className="flex-1 flex items-center gap-4 text-left active:scale-95 transition-transform"
                      >
                        <div className={cn(
                          "w-12 h-12 rounded-2xl flex items-center justify-center transition-colors",
                          expandedScriptId === script.id ? "bg-indigo-500 text-white" : "bg-indigo-50 text-indigo-500"
                        )}>
                          <ChevronRight size={24} />
                        </div>
                        <span className="font-bold text-slate-700 text-lg">{script.title}</span>
                      </button>
                      
                      <button
                        onClick={() => toggleScriptExpansion(script.id)}
                        className={cn(
                          "w-10 h-10 rounded-full flex items-center justify-center transition-all",
                          expandedScriptId === script.id ? "bg-indigo-100 text-indigo-600 rotate-180" : "bg-slate-50 text-slate-400 hover:bg-slate-100"
                        )}
                      >
                        <ChevronDown size={20} />
                      </button>
                    </div>

                    <AnimatePresence>
                      {expandedScriptId === script.id && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: "auto", opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          className="px-5 pb-6 pt-0 border-t border-slate-50"
                        >
                          <div className="pt-4 space-y-4">
                            <div className="flex items-center gap-2 text-slate-400">
                              <ListChecks size={14} />
                              <span className="text-[10px] uppercase font-black tracking-widest">Script Preview</span>
                            </div>
                            
                            {scriptDetails[script.id] ? (
                              <ul className="space-y-3">
                                {scriptDetails[script.id].questions.map((q: any, idx: number) => (
                                  <motion.li 
                                    key={idx}
                                    initial={{ opacity: 0, x: -10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: idx * 0.05 }}
                                    className="flex gap-3 text-sm text-slate-600 group"
                                  >
                                    <span className="flex-shrink-0 w-6 h-6 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-center text-[10px] font-bold text-slate-400 group-hover:bg-indigo-50 group-hover:text-indigo-500 transition-colors">
                                      {idx + 1}
                                    </span>
                                    <span className="pt-0.5 leading-relaxed">{q.text}</span>
                                  </motion.li>
                                ))}
                              </ul>
                            ) : (
                              <div className="flex items-center gap-2 py-2">
                                <div className="w-4 h-4 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
                                <span className="text-xs text-slate-400 font-medium">Loading questions...</span>
                              </div>
                            )}

                            <button
                              onClick={() => startSession(script.title)}
                              className="w-full mt-4 py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl text-xs font-bold transition-all active:scale-95 shadow-lg shadow-indigo-200"
                            >
                              Start This Reflection
                            </button>
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                </div>
              ))}
              
              {scripts.length === 0 && (
                <div className="text-center py-10 text-slate-400 italic">
                  Loading available paths...
                </div>
              )}
            </div>
          </motion.div>
        ) : (
          <motion.div
            key="chat"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex-1 flex flex-col overflow-hidden"
          >
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-8 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] bg-fixed">
              <AnimatePresence mode='popLayout'>
                {messages.length === 0 && (
                  <motion.div 
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                    className="text-center py-16 px-6"
                  >
                    <div className="bg-gradient-to-br from-indigo-500 to-purple-600 w-24 h-24 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-2xl rotate-6 hover:rotate-0 transition-transform duration-300">
                      <Bot size={48} className="text-white" />
                    </div>
                    <h2 className="text-2xl font-bold text-slate-800 mb-3">Welcome to {selectedScript}</h2>
                    <p className="text-slate-500 max-w-sm mx-auto leading-relaxed">
                      I'm ready to guide you. Just say hello to begin.
                    </p>
                  </motion.div>
                )}

                {messages.map((msg, i) => (
                  <motion.div
                    key={i}
                    layout
                    initial={{ opacity: 0, x: msg.role === 'user' ? 20 : -20, scale: 0.9 }}
                    animate={{ opacity: 1, x: 0, scale: 1 }}
                    className={cn(
                      "flex w-full px-2",
                      msg.role === 'user' ? "justify-end" : "justify-start"
                    )}
                  >
                    <div className={cn(
                      "flex max-w-[90%]",
                      msg.role === 'user' ? "flex-row-reverse" : "flex-row"
                    )}>
                      <div className={cn(
                        "w-10 h-10 rounded-2xl flex items-center justify-center flex-shrink-0 mt-1 shadow-lg border",
                        msg.role === 'user' ? "ml-3 bg-white border-slate-200" : "mr-3 bg-gradient-to-br from-indigo-600 to-purple-700 text-white border-white/20"
                      )}>
                        {msg.role === 'user' ? <User size={20} className="text-slate-600" /> : <Bot size={20} />}
                      </div>
                      
                      <div className="space-y-2">
                        <div className={cn(
                          "p-4 rounded-2xl shadow-sm text-[15px] leading-relaxed",
                          msg.role === 'user' 
                            ? "bg-slate-900 text-slate-50 rounded-tr-none border-b-2 border-indigo-500" 
                            : "bg-white border border-slate-100 rounded-tl-none text-slate-800 shadow-xl shadow-slate-200/50"
                        )}>
                          {msg.content}
                        </div>
                        
                        {/* Logic Debug Info */}
                        {msg.role === 'avatar' && msg.action && (
                          <motion.div 
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="flex gap-2 px-1"
                          >
                            <span className={cn(
                              "text-[9px] uppercase font-black px-2 py-1 rounded-full tracking-tighter border",
                              msg.action === 'NEXT' ? "bg-emerald-50 text-emerald-600 border-emerald-100" :
                              msg.action === 'ACKNOWLEDGE' ? "bg-indigo-50 text-indigo-600 border-indigo-100" :
                              "bg-amber-50 text-amber-600 border-amber-100"
                            )}>
                              {msg.action} DECISION
                            </span>
                          </motion.div>
                        )}
                      </div>
                    </div>
                  </motion.div>
                ))}
                
                {isLoading && (
                  <motion.div 
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="px-6 py-2"
                  >
                    <div className="flex gap-1.5 items-center">
                      <div className="flex gap-1 bg-slate-200/50 p-3 rounded-full">
                        <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                        <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                        <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                      </div>
                      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Processing</span>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
              <div ref={messagesEndRef} className="h-4" />
            </div>

            {/* Input Area */}
            <div className="p-6 bg-white border-t relative shadow-[0_-4px_20px_rgba(0,0,0,0.03)] focus-within:shadow-[0_-4px_25px_rgba(0,0,0,0.08)] transition-shadow duration-300">
              <form onSubmit={handleSend} className="relative group">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  disabled={isLoading || isSessionFinished}
                  placeholder={isSessionFinished ? "Session completed. Feel free to start a new path." : "Share your thoughts..."}
                  className={cn(
                    "w-full pl-6 pr-14 py-4 bg-slate-100 border-2 border-transparent rounded-3xl text-sm font-medium focus:bg-white focus:border-indigo-500 transition-all outline-none text-slate-800 placeholder:text-slate-400",
                    isSessionFinished && "bg-slate-50 opacity-70 cursor-not-allowed"
                  )}
                />
                <button
                  type="submit"
                  disabled={isLoading || !input.trim() || isSessionFinished}
                  className="absolute right-2 top-2 bottom-2 aspect-square text-white bg-gradient-to-br from-indigo-600 to-purple-600 rounded-2xl flex items-center justify-center hover:shadow-lg hover:shadow-indigo-200 disabled:from-slate-300 disabled:to-slate-400 disabled:shadow-none transition-all active:scale-90"
                >
                  <Send size={20} />
                </button>
              </form>
              <div className="flex justify-center mt-3">
                {isSessionFinished ? (
                   <span className="text-[10px] uppercase font-black text-indigo-500 tracking-widest animate-pulse">Session Successfully Ended</span>
                ) : (
                  <div className="h-1 w-12 bg-slate-200 rounded-full" />
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
