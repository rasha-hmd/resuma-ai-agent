import React, { useState, useEffect } from 'react';
import { Upload, FileText, Target, Award, BookOpen, BarChart3, Users, TrendingUp, Download, CheckCircle, AlertCircle, Moon, Sun, Menu, X, ExternalLink, Star, Clock, User, Settings } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar } from 'recharts';



// Main App Component
const App = () => {
  const [currentPage, setCurrentPage] = useState('home');
  const [darkMode, setDarkMode] = useState(false);
  const [results, setResults] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [resumeFile, setResumeFile] = React.useState(null);
  const [jobFile, setJobFile] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [matchResults, setMatchResults] = React.useState(null);
useEffect(() => {
  window.setResults = setResults;
  window.setCurrentPage = setCurrentPage;
}, []);



  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const handleOptimize = async (resumeFile, jobDescription) => {
  setIsLoading(true);
  const formData = new FormData();
  formData.append('resume_file', resumeFile);
  formData.append('job_description', jobDescription);


  try {
    const response = await fetch('http://localhost:8000/upload/', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) throw new Error('Upload failed');

    const data = await response.json();
    console.log("✅ Backend response:", data);
    setResults(data);
    setCurrentPage('results');
  } catch (error) {
    console.error('Error:', error);
    alert('Failed to process resume.');
  } finally {
    setIsLoading(false);
  }
};


  return (
    <div className={`min-h-screen ${darkMode ? 'dark bg-gray-900' : 'bg-gray-50'}`}>
      <Navigation
        currentPage={currentPage}
        setCurrentPage={setCurrentPage}
        darkMode={darkMode}
        toggleDarkMode={toggleDarkMode}
        mobileMenuOpen={mobileMenuOpen}
        setMobileMenuOpen={setMobileMenuOpen}
      />

      {isLoading && <LoadingOverlay />}

      <main className="pt-16">
        {currentPage === 'home' && <HomePage onOptimize={handleOptimize} darkMode={darkMode} />}
        {currentPage === 'results' && <ResultsPage results={results} darkMode={darkMode} />}
        {currentPage === 'cover-letter' && <CoverLetterPage results={results} darkMode={darkMode} />}
        {currentPage === 'rulebased' && <RuleBasedMatchPage darkMode={darkMode} />}
      </main>
    </div>
  );
};


// Navigation Component
const Navigation = ({ currentPage, setCurrentPage, darkMode, toggleDarkMode, mobileMenuOpen, setMobileMenuOpen }) => {
  const navItems = [
    { id: 'home', label: 'Home', icon: FileText },
    { id: 'results', label: 'Results', icon: BarChart3 },
    { id: 'cover-letter', label: 'Cover Letter', icon: BookOpen },
    { id: 'rulebased', label: 'Rule-Based Match', icon: Settings }
  ];

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 ${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} border-b backdrop-blur-sm bg-opacity-90`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Target className="h-8 w-8 text-blue-600 mr-2" />
            <span className={`text-xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Resuma
            </span>
          </div>

          <div className="hidden md:flex items-center space-x-8">
            {navItems.map(item => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => setCurrentPage(item.id)}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    currentPage === item.id
                      ? 'text-blue-600 bg-blue-50 dark:bg-blue-900 dark:text-blue-400'
                      : `${darkMode ? 'text-gray-300 hover:text-white' : 'text-gray-700 hover:text-gray-900'}`
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </div>

          <div className="flex items-center space-x-4">
            <button
              onClick={toggleDarkMode}
              className={`p-2 rounded-md ${darkMode ? 'text-gray-300 hover:text-white' : 'text-gray-700 hover:text-gray-900'}`}
            >
              {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
            </button>

            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
            >
              {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {mobileMenuOpen && (
        <div className={`md:hidden ${darkMode ? 'bg-gray-800' : 'bg-white'} border-t border-gray-200`}>
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {navItems.map(item => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setCurrentPage(item.id);
                    setMobileMenuOpen(false);
                  }}
                  className={`flex items-center space-x-2 w-full px-3 py-2 rounded-md text-base font-medium ${
                    currentPage === item.id
                      ? 'text-blue-600 bg-blue-50'
                      : `${darkMode ? 'text-gray-300 hover:text-white' : 'text-gray-700 hover:text-gray-900'}`
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      )}
    </nav>
  );
};

// Loading Overlay Component
const LoadingOverlay = () => (
  <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div className="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-xl text-center">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
      <p className="text-lg font-medium text-gray-900 dark:text-white">Optimizing your resume...</p>
      <p className="text-sm text-gray-500 dark:text-gray-400">This may take a few moments</p>
    </div>
  </div>
);

// Homepage Component
const HomePage = ({ onOptimize, darkMode }) => {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const file = e.dataTransfer.files[0];
    if (file && file.type === 'application/pdf') {
      setResumeFile(file);
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setResumeFile(file);
    }
  };

  const handleSubmit = () => {
    if (resumeFile && jobDescription.trim()) {
      onOptimize(resumeFile, jobDescription);
    }
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className={`py-20 ${darkMode ? 'bg-gray-900' : 'bg-gradient-to-br from-blue-50 to-indigo-100'}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className={`text-4xl md:text-6xl font-bold mb-6 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Empower Your Resume with{' '}
              <span className="text-blue-600">AI</span>
            </h1>
            <p className={`text-xl md:text-2xl mb-8 ${darkMode ? 'text-gray-300' : 'text-gray-600'} max-w-3xl mx-auto`}>
              Upload, Optimize, and Stand Out in today's competitive job market
            </p>
            <div className="flex justify-center space-x-6 mb-12">
              <div className="flex items-center space-x-2">
                <CheckCircle className="h-6 w-6 text-green-500" />
                <span className={`${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>AI-Powered Analysis</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle className="h-6 w-6 text-green-500" />
                <span className={`${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>Instant Feedback</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle className="h-6 w-6 text-green-500" />
                <span className={`${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>Job-Specific Optimization</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Upload Section */}
      <section className={`py-16 ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-8">
            {/* File Upload */}
            <div>
              <h2 className={`text-2xl font-bold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                Upload Your Resume
              </h2>
              <div
                className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                  dragActive
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900'
                    : `${darkMode ? 'border-gray-600 bg-gray-700' : 'border-gray-300 bg-gray-50'}`
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <Upload className={`mx-auto h-12 w-12 mb-4 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`} />
                {resumeFile ? (
                  <div>
                    <p className={`text-lg font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                      {resumeFile.name}
                    </p>
                    <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                      PDF uploaded successfully
                    </p>
                  </div>
                ) : (
                  <div>
                    <p className={`text-lg font-medium mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                      Drag & drop your resume here
                    </p>
                    <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'} mb-4`}>
                      PDF files only, max 10MB
                    </p>
                    <input
                      type="file"
                      accept=".pdf"
                      onChange={handleFileSelect}
                      className="hidden"
                      id="resume-upload"
                    />
                    <label
                      htmlFor="resume-upload"
                      className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 cursor-pointer transition-colors"
                    >
                      <Upload className="h-4 w-4 mr-2" />
                      Browse Files
                    </label>
                  </div>
                )}
              </div>
            </div>

            {/* Job Description */}
            <div>
              <h2 className={`text-2xl font-bold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                Job Description
              </h2>
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the job description here..."
                className={`w-full h-64 p-4 border rounded-lg resize-none ${
                  darkMode
                    ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400'
                    : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500'
                } focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
              />
              <p className={`text-sm mt-2 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                Copy and paste the complete job posting for better optimization results
              </p>
            </div>
          </div>

          {/* Optimize Button */}
          <div className="text-center mt-12">
            <button
              onClick={handleSubmit}
              disabled={!resumeFile || !jobDescription.trim()}
              className={`inline-flex items-center px-8 py-4 text-lg font-medium rounded-lg transition-all transform hover:scale-105 ${
                resumeFile && jobDescription.trim()
                  ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-lg'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }`}
            >
              <Target className="h-5 w-5 mr-2" />
              Optimize My Resume
            </button>
          </div>
        </div>
      </section>
    </div>
  );
};

// Results Page Component
const ResultsPage = ({ results, darkMode }) => {
  if (!results) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className={`text-lg ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
            No results available. Please upload a resume first.
          </p>
        </div>
      </div>
    );
  }

  const CircularProgress = ({ percentage, size = 200 }) => {
    const radius = (size - 20) / 2;
    const circumference = 2 * Math.PI * radius;
    const strokeDashoffset = circumference - (percentage / 100) * circumference;

    return (
      <div className="relative">
        <svg width={size} height={size} className="transform -rotate-90 translate-x-[50px]">
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={darkMode ? '#374151' : '#E5E7EB'}
            strokeWidth="10"
            fill="none"
          />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#3B82F6"
            strokeWidth="10"
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <div className={`text-4xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              {percentage}%
            </div>
            <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
              Match Score
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className={`min-h-screen py-8 ${darkMode ? 'bg-gray-900' : 'bg-gray-50'}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className={`text-4xl font-bold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            Resume Analysis Results
          </h1>
          <p className={`text-lg ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
            Here's how your resume matches the job requirements
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Match Score */}
          <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-8 text-center`}>
            <CircularProgress percentage={results.matchScore} />
            <h3 className={`text-xl font-semibold mt-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Overall Match
            </h3>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'} mt-2`}>
              Your resume compatibility with the job posting
            </p>
          </div>

          {/* Missing Keywords */}
          <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-8`}>
            <div className="flex items-center mb-6">
              <AlertCircle className="h-6 w-6 text-orange-500 mr-2" />
              <h3 className={`text-xl font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                Missing Keywords
              </h3>
            </div>
            <div className="space-y-2">
              {results.missingKeywords.map((keyword, index) => (
                <span
                  key={index}
                  className="inline-block bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-sm mr-2 mb-2"
                >
                  {keyword}
                </span>
              ))}
            </div>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'} mt-4`}>
              Consider adding these keywords to improve your match score
            </p>
          </div>

          {/* Improvements */}
          <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-8`}>
            <div className="flex items-center mb-6">
              <Award className="h-6 w-6 text-blue-500 mr-2" />
              <h3 className={`text-xl font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                Improvements
              </h3>
            </div>
            <ul className="space-y-3">
              {results.improvements.map((improvement, index) => (
                <li key={index} className="flex items-start">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
                  <span className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                    {improvement}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Download Button */}
        <div className="text-center mt-12">
  <a
    href="http://localhost:8000/download/final_resume_pdf"
    download
    className="inline-flex items-center px-8 py-4 bg-green-600 hover:bg-green-700 text-white text-lg font-medium rounded-lg transition-colors shadow-lg"
  >
    <Download className="h-5 w-5 mr-2" />
    Download Optimized Resume
  </a>
</div>
      </div>
    </div>
  );
};

// Cover Letter Page Component
const CoverLetterPage = ({ results, darkMode }) => {
  if (!results) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className={`text-lg ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
            No cover letter generated. Please optimize your resume first.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen py-8 ${darkMode ? 'bg-gray-900' : 'bg-gray-50'}`}>
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className={`text-4xl font-bold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            AI-Generated Cover Letter
          </h1>
          <p className={`text-lg ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
            Personalized cover letter based on your resume and job posting
          </p>
        </div>

        {/* Cover Letter */}
        <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-8 mb-8`}>
          <div className="flex items-center justify-between mb-6">
            <h2 className={`text-2xl font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Your Cover Letter
            </h2>
            <a
  href="http://localhost:8000/output/cover_letter.txt" // Make sure this path is correct
  download
  className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
>
  <Download className="h-4 w-4 mr-2" />
  Download
</a>

          </div>
          <div className={`prose max-w-none ${darkMode ? 'prose-invert' : ''}`}>
            <div className={`whitespace-pre-line ${darkMode ? 'text-gray-300' : 'text-gray-700'} leading-relaxed`}>
              {results.coverLetter}
            </div>
          </div>
        </div>

        {/* Recommended Courses */}
        <div className="mb-8">
          <h2 className={`text-2xl font-semibold mb-6 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            Recommended Upskilling Courses
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {results.courses.map((course, index) => (
              <div key={index} className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow`}>
                <div className="flex items-center mb-4">
                  <BookOpen className="h-6 w-6 text-blue-500 mr-2" />
                  <span className={`text-sm font-medium ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                    {course.provider}
                  </span>
                </div>
                <h3 className={`text-lg font-semibold mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                  {course.title}
                </h3>

                <div className="flex items-center justify-between mb-4">

                </div>
                <div className="flex items-center justify-between">
                  <span className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                    {course.price}
                  </span>
                  <a
  href={course.link}
  target="_blank"
  rel="noopener noreferrer"
  className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-lg transition-colors"
>
  <ExternalLink className="h-4 w-4 mr-2" />
  Enroll Now
</a>

                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
const RuleBasedMatchPage = ({ darkMode }) => {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobFile, setJobFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [matchResults, setMatchResults] = useState(null);

  const handleMatch = async () => {
    if (!resumeFile || !jobFile) {
      alert("Please upload both resume and job description files");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("resume_file", resumeFile);
    formData.append("job_file", jobFile);

    try {
      const response = await fetch("http://127.0.0.1:8000/rulebased", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to fetch match results");
      }

      const data = await response.json();
      setMatchResults(data);
    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  // Helper to safely render sets or arrays
  const renderItems = (items) => {
    if (!items) return "None";
    if (Array.isArray(items)) return items.join(", ");
    if (items instanceof Object && typeof items[Symbol.iterator] === "function") {
      return Array.from(items).join(", ");
    }
    return String(items);
  };

  return (
    <div className={`p-6 ${darkMode ? "bg-gray-900 text-white" : "bg-white text-black"}`}>
      <h1 className="text-3xl font-bold mb-4">📄 Resume vs Job Matcher</h1>

      <div className="flex flex-col md:flex-row gap-4 mb-6">
        <input type="file" accept=".pdf" onChange={(e) => setResumeFile(e.target.files[0])} />
        <input type="file" accept=".txt" onChange={(e) => setJobFile(e.target.files[0])} />
        <button
          onClick={handleMatch}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          disabled={loading}
        >
          Match Now
        </button>
      </div>

      {loading && <p>🔍 Analyzing...</p>}

      {matchResults && (
  <div className="mt-6">
    <h2 className="text-xl font-semibold mb-2">Match Results</h2>

    <p>
      <strong>Weighted Score:</strong>{" "}
      {typeof matchResults.weighted_score === "number"
        ? matchResults.weighted_score.toFixed(2)
        : "N/A"}
      %
    </p>
    <p>
      <strong>Simple Score:</strong>{" "}
      {typeof matchResults.simple_score === "number"
        ? matchResults.simple_score.toFixed(2)
        : "N/A"}
      %
    </p>

    <div className="mt-4">
      <h3 className="font-semibold">Category Breakdown:</h3>
      {matchResults.category_results &&
        Object.entries(matchResults.category_results).map(([cat, data]) => (
          <div key={cat} className="mb-2">
            <p className="font-bold">{cat.toUpperCase()}</p>
            <p>Score: {typeof data.score === "number" ? data.score.toFixed(2) : "N/A"}%</p>
            <p>Matched: {renderItems(data.matched)}</p>
            <p>Missing: {renderItems(data.missing).split(", ").slice(0, 10).join(", ")}</p>
          </div>
        ))}
    </div>

    <div className="mt-4">
      <h3 className="font-semibold">Top Matched Keywords:</h3>
      <p>{renderItems(matchResults.overall_matched).split(", ").slice(0, 15).join(", ")}</p>
    </div>

    <div className="mt-4">
      <h3 className="font-semibold">Recommendation:</h3>
      <p>{matchResults.recommendation}</p>
    </div>
  </div>
)}

    </div>
  );

};


export default App;