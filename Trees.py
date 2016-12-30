"""

Puu tietorakenteisiin liittyvät luokkamäärittelyt

"""

class Tree:
    """ Abstrakti Puu-luokka """

    class Position:
        """
            Abstraktio luokasta kuvaamaan tiettyä solmua puussa.
            Käytetään jatkossa lyhennettä p = position ja
            termiä sijainti kuvaamaan instanssia tästä luokasta.
        """

        def element(self):
            """ palauttaa tälle sijainnille tallennetun elementin """
            raise NotImplementedError('must be implemented by subclass')

        def __eq__(self, other):
            """
                Palauttaa: Tosi, jos toinen positio kuvaa samaa paikkaa
                käytännössä siis: self.equal(other)
            """
            raise NotImplementedError('must be implemented by subclass')

        def __ne__(self, other):
            """
                Palauttaa: Tosi, jos other ei kuvaa samaa paikkaa
                käytännössä siis: self.not_equal(other)
            """
            return not (self == other)

    """ Puun abstraktit metodit """

    def root(self):
        """ Palauttaa puun juurisolmun tai (tai None jos juurta) """
        raise NotImplementedError('must be implemented by subclass')

    def parent(self, p):
        """ Palauttaa p:n vanhemman sijainnin (tai None jos ei vanhempaa) """
        raise NotImplementedError('must be implemented by subclass')

    def num_children(self, p):
        """ Palauttaa p:n lasten lukumäärän """
        NotImplementedError('must be implemented by subclass')

    def children(self, p):
        """ Luodaan iteraatio p:n lasten solmuista """
        NotImplementedError('must be implemented by subclass')

    def __len__(self):
        """ Palauttaa puun kaikkien solmujen summan """
        NotImplementedError('must be implemented by subclass')

    def __iter__(self):
        """ Luodaan iteraatio puun elementeistä """
        for p in self.positions():
            yield p.element()

    """ Puun läpikäyntialgoritmit """

    def preorder(self):
        """ 'ennakkojärjestys' -iteraatio """
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):
                yield p

    def _subtree_preorder(self, p):
        """ 'ennakkojärjestys' -iteraatio p:n alipuille """
        yield p
        for c in self.children(p):
            for other in self._subtree_preorder(c):
                yield other

    def postorder(self):
        """ 'jälkijärjestys' -iteraatio """
        if not self.is_empty():
            for p in self._subtree_postorder(self.root()):
                yield p

    def _subtree_postorder(self, p):
        """ 'jälkijärjestys' -iteraatio p:n alipuillle """
        for c in self.children(p):
            for other in self._subtree_postorder(c):
                yield other
            yield p

    def positions(self):
        """ luodaan iteraatio puun sijainneista """
        return self.preorder()

    """ Puun konkreettiset metodit """

    def is_root(self, p):
        """ Palauttaa: Tosi, jos p on puun juuri """
        return self.root() == p

    def is_leaf(self, p):
        """ Palauttaa: Tosi, jos p:llä ei lapsia """
        return self.num_children() == 0

    def is_empty(self):
        """ Palauttaa: Tosi, jos puu on tyhjä """
        return len(self) == 0

    def depth(self, p):
        """ Palauttaa p:tä ja juurta erottavien tasojen määrän """
        if self.is_root():
            return 0
        else:
            # tehdään rekursiivisesti kunnes p == is_root()
            # aikakompleksisuus O(depth_of_p + 1)
            return 1 + self.depth(self.parent(p))

    def _height(self, p):
        """ Palauttaa p:lle juurrutetun alipuun korkeuden"""
        if self.is_leaf(p):
            return 0
        else:
            return 1 + max(self._height(c) for c in self.children(p))

    def height(self, p=None):
        """ Palauttaa p:lle juurrutetun alipuun korkeuden JOS p ei None,
            silloin palautetaan koko puun korkeus.
        """
        if p is None:
            p = self.root()
        return self._height(p)


class BinaryTree(Tree):
    """ Abstrakti Binääripuu-luokka. Eroaa puusta sillä, että solmulla voi olla vain kaksi lasta """

    # Lisätään abstrakteja metodeja täyttämään binäärisen puun tarpeet
    def left(self, p):
        """
            Palauttaa p:n vasemman lapsen, mutta jos
            ei vasenta lasta palautetaan None
        """
        NotImplementedError('must be implemented by subclass')

    def right(self, p):
        """
            Palauttaa p:n oikean lapsen, mutta jos
            ei oikeaa lasta palautetaan None
        """
        NotImplementedError('must be implemented by subclass')

    # Luokan implementoimat konkreettiset metodit

    def sibling(self, p):
        """ Palauttaa p:n sisaren solmun jos sellainen olemassa """
        parent = self.parent(p)
        if parent is None:
            return None
        else:
            # kumpikin seuraavista palautuksista voi
            # olla mahdollisesti None
            if p == self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)

    def children(self, p):
        """
            Implementoidaan Tree-luokan children() metodi.
            Luodaan iteraatio p:n lasten solmuista
        """
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)



class LinkedBinaryTree(BinaryTree):
    """ Linkitetty versio Binääripuu -tietorakenteesta """

    class _Node:
        __slots__ = '_element', '_parent', '_left', '_right'

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    class Position(BinaryTree.Position):
        """ Abstraktio kuvaamaan elementin solmua """

        def __init__(self, container, node):
            """ Käyttäjän ei tulisi käyttää tätä konstruktoria """
            self._container = container
            self._node = node

        """ Implementoidaan Tree.Position -luokassa määritellyt metodit """

        def element(self):
            return self._node._element

        def __eq__(self, other):
            return type(other) is type(self) and other._node is self._node

        def _validate(self, p):
            """ palautetaan solmu jos sijainti p validi """

            if not isinstance(p, self.Position):
                raise TypeError('p must be proper Position type')
            if p._container is not self:
                raise ValueError('p does not belong to this container')
            if p._node._parent is p._node:
                raise ValueError('p is no longer valid')
            return p._node

        def _make_position(self, node):
            """
            :param node:
            :return: node:n Position instanssi
            """
            return self.Position(self, node) if node is not None else None


    # Binääripuun konstruktori

    def __init__(self):
        """ Luodaan tyhjä binääripuu """
        self._root = None
        self._size = 0

    # Implementoidaan Pääluokan julkiset metodit

    def __len__(self):
        """ Palautetaan puun elementtien lukumäärä """
        return self._size

    def root(self):
        """ Palautetaan juuren sijainti """
        return self._make_position(self._root)

    def parent(self, p):
        """ Palautetaan p:n vanhemman sijainti (tai None jos p on juuri) """
        node = self._validate(p)
        return self._make_position(node._parent)

    def left(self, p):
        """ Palautetaan p:n vasemman lapsen sijainti (tai None jos ei vasenta lasta) """
        node = self._validate(p)
        return self._make_position(node._left)

    def right(self, p):
        """ Palautetaan p:n oikean lapsen sijainti (tai None jos ei oikeaa lasta) """
        node = self._validate(p)
        return self._make_position(node._right)

    def num_children(self, p):
        """ Palautetaan sijainnin p lasten lukumäärä """
        node = self._validate(p)
        count = 0
        if node._left is not None:
            count += 1
        if node._right is not None:
            count += 1
        return count


    # Luokan yksityiset päivitysmetodit

    def _add_root(self, e):
        """ Sijoitetaan elementti e juureksi ja palautetaan sen sijainti """

        if self._root is not None: raise ValueError('Root exists')
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)

    def _add_left(self, p, e):
        """ Luodaan uusi vasen lapsi sijaintiin p ja sijoitetaan elementti e """

        node = self._validate(p)
        if node._left is not None: raise ValueError('Left child exists')
        self._size += 1
        node._left = self._Node(e, node)
        return self._make_position(node._left)

    def _add_righ(self, p, e):
        """ Luodaan uusi oikea lapsi sijaintiin p ja sijoitetaan elementti e """

        node = self._validate(p)
        if node._righ is not None: raise ValueError('righ child exists')
        self._size += 1
        node._right= self._Node(e, node)
        return self._make_position(node._right)

    def _replace(self, p, e):
        """ Korvaa sijainnin p elementti e:llä ja palauta korvattu elementti """

        node = self._validate(p)
        old = node._element
        node._element = e
        return old

    def _delete(self, p):
        """
            Poista solmu sijainnista p, ja korvaa se p:n lapsella jos sellainen olemassa.
            Palauta sijainnissa p ollut elementti.
            Nosta "ValueError" jos p ei ole validi tai jos sillä on useampi lapsi
        """

        node = self._validate(p)
        if self.num_children(p) == 2: raise ValueError('p has two children')
        child = node._left if node._left else node._right
        if child is not None:
            child._parent = node._parent
        if node is self._root:
            self._root = child
        else:
            parent = node._parent
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1
        node._parent = node
        return node._element

    def _attach(self, p, t1, t2):
        """ Yhdistä puut t1 ja t2 p:n alipuiksi """

        node = self._validate(p)
        if not self.is_leaf(p): raise ValueError('position must be leaf')
        if not type(self) is type(t1) is type(t2):
            raise TypeError('Tree types must match')
        self._size += len(t1) + len(t2)
        if not t1.is_empty():
            t1._root._parent = node
            node._left = t1._root
            t1._root = None
            t1._size = 0
        if not t2.is_empty():
            t2._root._parent = node
            node._right = t2._root
            t2._root = None
            t2._size = 0








