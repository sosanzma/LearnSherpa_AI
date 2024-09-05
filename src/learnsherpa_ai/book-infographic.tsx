import React, { useState } from 'react';
import { Book } from 'lucide-react';
import { Card, CardHeader, CardContent } from '@/components/ui/card';

const books = [
  {
    title: "Theoretical Neuroscience",
    author: "Peter Dayan and L.F. Abbott",
    summary: "Introduces mathematical and computational methods in theoretical neuroscience.",
    opinion: "Praised for clarity and depth, suitable for beginners and experts."
  },
  {
    title: "Genome",
    author: "Matt Ridley",
    summary: "Explores genetic discoveries and their implications for human behavior and evolution.",
    opinion: "Acclaimed for making complex genetic concepts accessible to a general audience."
  },
  {
    title: "Sapiens",
    author: "Yuval Noah Harari",
    summary: "Surveys human history from the Stone Age to modern era, exploring biology and history.",
    opinion: "Lauded for its sweeping narrative and connection of historical events to contemporary issues."
  },
  {
    title: "Man's Search for Meaning",
    author: "Viktor Frankl",
    summary: "Details Frankl's experiences as a Holocaust survivor and psychological insights gained.",
    opinion: "Described as haunting yet uplifting, providing deep insights into the human condition."
  },
  {
    title: "The Brain That Changes Itself",
    author: "Norman Doidge",
    summary: "Explores neuroplasticity and the brain's ability to adapt and heal.",
    opinion: "Praised for challenging conventional views of the brain's capabilities."
  },
  {
    title: "The Man Who Mistook His Wife for a Hat",
    author: "Oliver Sacks",
    summary: "Presents complex neurological case studies with compassion and insight.",
    opinion: "Captivates readers with its blend of storytelling and scientific insight."
  },
  {
    title: "Descartes' Error",
    author: "Antonio Damasio",
    summary: "Challenges the dichotomy between emotion and reason in decision-making.",
    opinion: "Recognized for its intellectual rigor and reshaping understanding of emotions in cognition."
  }
];

const BookCard = ({ book }) => (
  <Card className="w-full max-w-md mb-4">
    <CardHeader className="flex flex-row items-center gap-2">
      <Book className="h-6 w-6" />
      <h3 className="text-lg font-semibold">{book.title}</h3>
    </CardHeader>
    <CardContent>
      <p className="text-sm text-gray-600 mb-2">by {book.author}</p>
      <p className="mb-2">{book.summary}</p>
      <p className="text-sm italic">{book.opinion}</p>
    </CardContent>
  </Card>
);

const BookInfographic = () => {
  const [selectedBook, setSelectedBook] = useState(null);

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Comprehensive Book Report</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {books.map((book, index) => (
          <div
            key={index}
            className="cursor-pointer"
            onClick={() => setSelectedBook(book)}
          >
            <BookCard book={book} />
          </div>
        ))}
      </div>
      {selectedBook && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg p-6 max-w-2xl w-full">
            <h3 className="text-xl font-bold mb-2">{selectedBook.title}</h3>
            <p className="text-gray-600 mb-4">by {selectedBook.author}</p>
            <p className="mb-4">{selectedBook.summary}</p>
            <p className="italic mb-4">{selectedBook.opinion}</p>
            <button
              className="bg-blue-500 text-white px-4 py-2 rounded"
              onClick={() => setSelectedBook(null)}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default BookInfographic;
