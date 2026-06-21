import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ChevronRight, ArrowLeft, Package, Sparkles } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const SKINCARE_QUESTIONS = [
  {
    id: 'q1',
    text: 'How does your skin feel a few hours after washing?',
    options: [
      { id: 'A', text: 'Tight, dry, or showing flakes' },
      { id: 'B', text: 'Comfortable and balanced' },
      { id: 'C', text: 'Shiny, greasy, or oily all over' },
      { id: 'D', text: 'Red, itchy, burning, or irritated' }
    ]
  },
  {
    id: 'q2',
    text: 'How visible are the pores on your face?',
    options: [
      { id: 'A', text: 'Barely visible' },
      { id: 'B', text: 'Large and visible all over' },
      { id: 'C', text: 'Visible mostly on my nose, forehead, and chin (T-zone)' },
      { id: 'D', text: 'Small to medium, but skin often looks red or blotchy' }
    ]
  },
  {
    id: 'q3',
    text: 'How does your face look or feel by midday?',
    options: [
      { id: 'A', text: 'Dull, tight, or with rough patches' },
      { id: 'B', text: 'Extremely shiny and greasy' },
      { id: 'C', text: 'Shiny only in the T-zone' },
      { id: 'D', text: 'Red, hot, or irritated by makeup/skincare' }
    ]
  },
  {
    id: 'q4',
    text: 'What is your skin\'s reaction to trying a new product?',
    options: [
      { id: 'A', text: 'Rarely reacts, but feels dry if not rich enough' },
      { id: 'B', text: 'Sometimes breaks out, but handles it fine overall' },
      { id: 'C', text: 'Easily gets red, burns, or breaks out in hives' },
      { id: 'D', text: 'Different parts of my face react differently' }
    ]
  },
  {
    id: 'q5',
    text: 'Do you experience visible flaking or rough patches?',
    options: [
      { id: 'A', text: 'Yes, frequently all over my face' },
      { id: 'B', text: 'Almost never, skin is smooth but shiny' },
      { id: 'C', text: 'Only occasionally around my mouth or cheeks' },
      { id: 'D', text: 'Yes, accompanied by redness and irritation' }
    ]
  }
];

const HAIRCARE_QUESTIONS = [
  // Scalp
  {
    id: 'hq1',
    text: 'How does your scalp feel by the end of the day after washing?',
    options: [
      { id: 'A', text: 'Clean, but maybe a bit dry or itchy' },
      { id: 'B', text: 'Greasy and oily, hair looks flat at the roots' }
    ]
  },
  {
    id: 'hq2',
    text: 'How often do you need to wash your hair to keep it looking clean?',
    options: [
      { id: 'A', text: 'Every 3-4 days or longer' },
      { id: 'B', text: 'Every day or every other day' }
    ]
  },
  {
    id: 'hq3',
    text: 'Do you experience flaking or itchiness?',
    options: [
      { id: 'A', text: 'Yes, dry white flakes that fall easily, and itchy' },
      { id: 'B', text: 'Yes, oily/waxy yellowish flakes that stick, or minimal flaking' }
    ]
  },
  // Porosity
  {
    id: 'hq4',
    text: 'How does your hair respond when you apply hair oils or leave-in serums?',
    options: [
      { id: 'A', text: 'The oil sits on top of my hair for a long time and doesn\'t absorb easily' },
      { id: 'B', text: 'It absorbs well and makes my hair feel soft and hydrated' },
      { id: 'C', text: 'It absorbs instantly, but my hair feels dry and thirsty again soon after' }
    ]
  },
  {
    id: 'hq5',
    text: 'How long does it take for your hair to dry naturally (without a hair dryer)?',
    options: [
      { id: 'A', text: 'A very long time (several hours or all day)' },
      { id: 'B', text: 'A normal amount of time (2-3 hours)' },
      { id: 'C', text: 'Extremely fast (under an hour)' }
    ]
  },
  {
    id: 'hq6',
    text: 'When you spray a mist of water on a dry strand of hair, what happens?',
    options: [
      { id: 'A', text: 'The water drops bead up and sit on the surface of the hair' },
      { id: 'B', text: 'The water beads for a moment, then is gradually absorbed' },
      { id: 'C', text: 'The water is absorbed instantly' }
    ]
  },
  {
    id: 'hq7',
    text: 'How does your hair behave during or after chemical/color treatments?',
    options: [
      { id: 'A', text: 'It is very resistant to dye or takes a long time to process' },
      { id: 'B', text: 'It takes color easily and retains it well' },
      { id: 'C', text: 'It takes color very fast, but fades quickly and feels damaged/porous' }
    ]
  }
];

export default function Quiz() {
  const { category } = useParams();
  const navigate = useNavigate();
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  // MODAL STATE
  const [showChoiceModal, setShowChoiceModal] = useState(false);
  const [quizData, setQuizData] = useState(null);

  const questions = category === 'skincare' ? SKINCARE_QUESTIONS : HAIRCARE_QUESTIONS;
  const currentQuestion = questions[currentIndex];

  const handleSelect = (optionId) => {
    setAnswers(prev => ({ ...prev, [currentQuestion.id]: optionId }));
  };

  const handleNext = async () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(prev => prev + 1);
    } else {
      setIsSubmitting(true);
      try {
        const response = await fetch(`${API_URL}/api/quiz/${category}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ session_id: 'user_123', answers })
        });
        const data = await response.json();
        setQuizData(data);
        setIsSubmitting(false);
        setShowChoiceModal(true);
      } catch (error) {
        console.error("Failed to submit quiz:", error);
        setIsSubmitting(false);
      }
    }
  };

  const handleBack = () => {
    if (currentIndex > 0) {
      setCurrentIndex(prev => prev - 1);
    } else {
      navigate('/');
    }
  };

  if (showChoiceModal) {
    return (
      <div className="w-full max-w-3xl mx-auto flex flex-col items-center justify-center py-10 px-4">
        <div className="glass-card dark:bg-slate-800/90 dark:border-slate-700 p-10 md:p-16 text-center w-full animate-in fade-in slide-in-from-bottom-4 duration-500">
          <Sparkles className="mx-auto w-20 h-20 mb-8 text-yellow-400" />
          <h2 className="text-4xl font-bold text-slate-800 dark:text-white mb-6">Analysis Complete!</h2>
          <p className="text-slate-600 dark:text-slate-400 mb-12 text-xl">What would you like to see for your recommended {category} routine?</p>
          
          <div className="grid md:grid-cols-2 gap-8">
            <button 
              onClick={() => navigate(`/results/${category}`, { state: { data: quizData, viewMode: 'products' } })}
              className={`p-8 rounded-3xl border-2 transition-all hover:-translate-y-2 flex flex-col items-center justify-center gap-6 ${category === 'skincare' ? 'border-indigo-200 dark:border-indigo-800 hover:border-indigo-500 hover:shadow-indigo-500/20 bg-indigo-50/30 dark:bg-indigo-900/20' : 'border-rose-200 dark:border-rose-800 hover:border-rose-500 hover:shadow-rose-500/20 bg-rose-50/30 dark:bg-rose-900/20'}`}
            >
              <Package size={48} className={category === 'skincare' ? 'text-indigo-500' : 'text-rose-500'} />
              <div className="space-y-2">
                <span className="text-2xl font-bold text-slate-800 dark:text-white block">Product Recommendations</span>
                <span className="text-md text-slate-500 block">Top curated market products</span>
              </div>
            </button>
            
            <button 
              onClick={() => navigate(`/results/${category}`, { state: { data: quizData, viewMode: 'remedies' } })}
              className="p-8 rounded-3xl border-2 border-emerald-200 dark:border-emerald-800 hover:border-emerald-500 hover:shadow-emerald-500/20 bg-emerald-50/30 dark:bg-emerald-900/20 transition-all hover:-translate-y-2 flex flex-col items-center justify-center gap-6"
            >
              <div className="w-12 h-12 rounded-full bg-emerald-100 dark:bg-emerald-900/50 text-emerald-600 dark:text-emerald-400 flex items-center justify-center font-bold text-xl">DIY</div>
              <div className="space-y-2">
                <span className="text-2xl font-bold text-slate-800 dark:text-white block">Home Remedies</span>
                <span className="text-md text-slate-500 block">Natural, easy DIY recipes</span>
              </div>
            </button>
          </div>
        </div>
      </div>
    );
  }

  const progress = ((currentIndex + 1) / questions.length) * 100;

  return (
    <div className="w-full max-w-2xl mx-auto flex flex-col">
      <div className="flex items-center justify-between mb-8">
        <button onClick={handleBack} className="flex items-center text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-white transition-colors">
          <ArrowLeft size={20} className="mr-1" /> Back
        </button>
        <span className="text-sm font-medium text-slate-400">
          Question {currentIndex + 1} of {questions.length}
        </span>
      </div>

      <div className="w-full h-2 bg-slate-200 dark:bg-slate-700 rounded-full mb-10 overflow-hidden">
        <div 
          className={`h-full transition-all duration-500 ${category === 'skincare' ? 'bg-indigo-500' : 'bg-rose-500'}`}
          style={{ width: `${progress}%` }}
        />
      </div>

      <div className="glass-card dark:bg-slate-800/80 dark:border-slate-700 p-8 md:p-10">
        <h2 className="text-2xl md:text-3xl font-bold text-slate-800 dark:text-white mb-8 leading-tight">
          {currentQuestion.text}
        </h2>

        <div className="space-y-4">
          {currentQuestion.options.map(option => {
            const isSelected = answers[currentQuestion.id] === option.id;
            return (
              <button
                key={option.id}
                onClick={() => handleSelect(option.id)}
                className={`w-full text-left p-5 rounded-xl border-2 transition-all duration-200 flex items-center justify-between ${
                  isSelected 
                  ? (category === 'skincare' ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/30 text-indigo-900 dark:text-indigo-100' : 'border-rose-500 bg-rose-50 dark:bg-rose-900/30 text-rose-900 dark:text-rose-100') 
                  : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:border-slate-300 dark:hover:border-slate-600 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700'
                }`}
              >
                <span className="text-lg font-medium">{option.text}</span>
                <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                  isSelected 
                  ? (category === 'skincare' ? 'border-indigo-500' : 'border-rose-500') 
                  : 'border-slate-300 dark:border-slate-600'
                }`}>
                  {isSelected && <div className={`w-3 h-3 rounded-full ${category === 'skincare' ? 'bg-indigo-500' : 'bg-rose-500'}`} />}
                </div>
              </button>
            )
          })}
        </div>

        <div className="mt-10 flex justify-end">
          <button
            onClick={handleNext}
            disabled={!answers[currentQuestion.id] || isSubmitting}
            className={`btn-primary flex items-center ${(!answers[currentQuestion.id] || isSubmitting) ? 'opacity-50 cursor-not-allowed' : ''} ${category === 'skincare' ? 'bg-indigo-600 hover:bg-indigo-700' : 'bg-rose-600 hover:bg-rose-700'}`}
          >
            {isSubmitting ? 'Analyzing...' : currentIndex === questions.length - 1 ? 'See Results' : 'Next Question'}
            {!isSubmitting && <ChevronRight size={20} className="ml-1" />}
          </button>
        </div>
      </div>
    </div>
  );
}
