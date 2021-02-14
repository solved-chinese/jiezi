import React from 'react';
import 'core-js/stable';
import 'regenerator-runtime/runtime';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import WordDefinition from './WordDefinition';
import ExampleSentences from './ExampleSentences';

import BreakdownView from '@learning.components/ItemDisplay/BreakdownView';
import LoadingView from '@learning.components/ItemDisplay/LoadingView.js';

import useLoadWord from '@learning.hooks/useLoadWord.js';

//Top and Bottom Containters
const ContainerTop = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    @media only screen and (max-width: 480) {
        flex-direction: column;
    }
`;

const ContainerBottom = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    @media only screen and (max-width: 768px) {
        flex-direction: column;
    }
`;

const ExampleSentenceHeading = styled.h2`
    color: var(--teritary-text);
    margin-top: 10px;
    font-size: 0.9em;
    font-weight: 400;
    text-align: center;
`;

/** The main function that renders a word view. */
export default function WordDisplay(props) {

    const word = props.word == null ?
        useLoadWord(
        props.url == null ?
            `/content/word/${props.qid}` : props.url
        ) : props.word;

    const renderWord = (word) => {
        const chinese = word.chinese;
        const pinyin = word.pinyin;
        const definitions = word.definitions;
        const audioURL = word.audioUrl;
        
        return (
            <>
                {/* Top: Word Definition*/}
                <ContainerTop>
                    <WordDefinition 
                        audioURL= {audioURL}
                        chinese={chinese}
                        pinyin={pinyin}
                        definitions={definitions}
                    />
                </ContainerTop>

                {/* Bottom: Example Sentences */}
                <ExampleSentenceHeading>
                    Example Sentences
                </ExampleSentenceHeading>
                <ContainerBottom>
                    {word.sentences.map((sen, i) => {
                        return (
                            <ExampleSentences
                                key={sen.chineseHighlight}
                                word={word}
                                pinyin={sen.pinyinHighlight}
                                audioURL={sen.audioUrl}
                                chinese={sen.chineseHighlight}
                                translation={sen.translationHighlight}
                            />
                        );
                    })}
                </ContainerBottom>
        
                {/* Show Breakdown toggle. Borrowed from Michael*/}
                <BreakdownView 
                    type='word'
                    componentURL={word.characters}
                    memoryAid={word.memoryAid}
                />
            </>
        );
    };

    if (word === null) {
        return <LoadingView />;
    } else {
        return renderWord(word);
    }
}

WordDisplay.propTypes = {
    /** The word object to be rendered, if not provides,
     *  url will be used to construct the object.
     */
    word: PropTypes.object,

    /** The URL of the word to be rendered, if it
     * is not provided, then the qid is used to construct
     * the url. */
    url: PropTypes.string,

    /** The query id of the word to be rendered, will
     * be omitted if url is present and not null. */
    qid: PropTypes.number,
};